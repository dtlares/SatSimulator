""" Module for task planning"""
from commands.command_factory import CommandFactory


class UnitTask:
    """ Task data type"""
    def __init__(self, cmd_type: CommandFactory.CommandType, payoff: int, resources: list):
        """ Task constructor"""
        self.type = cmd_type
        self.payoff = payoff
        self.resources = resources


class TasksPlanner:
    """ Task Planner functions"""
    @staticmethod
    def get_plan(set_count: int, tasks_list: list):
        """ Returns an optimized task plan"""
        # Find tasks that have non common resources
        non_common_tasks = set()
        non_common_gruped_tasks = dict()
        task_count = len(tasks_list)
        for i in range(0, task_count):
            non_common_gruped_tasks[i] = []
            task_a = tasks_list[i]
            added_tasks = []

            for j in range(0, task_count):

                if i == j:
                    continue

                task_b = tasks_list[j]

                resource_match = False

                for resource in task_a.resources:
                    if resource in task_b.resources:
                        resource_match = True
                        break

                if not resource_match:
                    min_task_index = min(i, j)
                    max_task_index = max(i, j)

                    added_tasks.append(min_task_index)
                    added_tasks.append(max_task_index)

                    non_common_gruped_tasks[i].append(j)
                    non_common_tasks.add(((min_task_index, max_task_index), task_a.payoff + task_b.payoff))

            # If the task is isolated, we need to add it to the non_common_group
            if i not in added_tasks:
                non_common_gruped_tasks[i].append(j)
                non_common_tasks.add((i, task_a.payoff))

        return TasksPlanner._merge_non_common_tasks(non_common_tasks, tasks_list, non_common_gruped_tasks, set_count)

    @staticmethod
    def _merge_non_common_tasks(non_common_tasks, tasks_list, non_common_gruped_tasks, set_count):
        """ Recursive function used to merge plans"""
        # Sort pairs by highest payoff sum
        non_common_tasks = sorted(non_common_tasks, key=lambda val: val[1], reverse=True)
        # Group by common non common tasks
        grouped_tasks = []
        used_tasks = []
        non_common_tasks_count = len(non_common_tasks)

        for i in range(0, non_common_tasks_count):

            task_arr = non_common_tasks[i][0]
            # if there is only element in the tuple, we append it at the end
            if isinstance(task_arr, int):
                grouped_tasks.append([task_arr, tasks_list[task_arr].payoff])
                continue

            # take the first item in the tuple
            task_a = task_arr[0]

            # Continue if the task is already used
            if task_a in used_tasks:
                continue

            # Get all the group of non-commons tasks with the task a
            tmp_grouped_tasks = non_common_gruped_tasks[task_a][:]

            # find all the occurrences between the non-common task of a and the non-common task of all tasks in the
            # group

            remainder_group = task_arr[1:]

            for task in remainder_group:
                set1 = set(tmp_grouped_tasks)
                set2 = set(non_common_gruped_tasks[task])

                # find the intersection
                tmp_grouped_tasks = list(set1 & set2)

            # Remove all elements that are already used
            if len(tmp_grouped_tasks) != 0:
                tmp_grouped_tasks[i] = [i for i in tmp_grouped_tasks if i not in used_tasks]

            # Add the already grouped tasks
            tmp_grouped_tasks.extend(non_common_tasks[i][0][:])

            # Compute the payoffs
            payoffs = [tasks_list[i].payoff for i in tmp_grouped_tasks]
            grouped_tasks.append([tuple(tmp_grouped_tasks), sum(payoffs)])

        # Sort pairs by highest payoff sum
        grouped_tasks = sorted(grouped_tasks, key=lambda val: val[1], reverse=True)
        final_tasks = []

        for group in grouped_tasks:
            group_list = [group[0]] if isinstance(group[0], int) else group[0]
            final_tasks.append([tasks_list[i] for i in group_list])

        if set_count < len(final_tasks) < len(non_common_tasks):
            final_tasks = TasksPlanner._merge_non_common_tasks(non_common_tasks, tasks_list, non_common_gruped_tasks,
                                                               set_count)

        return final_tasks[0: set_count]

    @staticmethod
    def build_commands(tasks: list, source: str, destination_list: list):
        """ Translates tasks into commands"""
        if len(destination_list) != len(tasks):
            return None

        cmd_list = []

        for i in range(0, len(tasks)):

            task_set = tasks[i]
            tmp_task = task_set if isinstance(task_set, list) else [task_set]
            tmp_cmd_list = []

            for task in tmp_task:
                new_cmd = CommandFactory.get_command(cmd_type=task.type, src=source, dest=destination_list[i],
                                                     param=[task.payoff, task.resources])

                tmp_cmd_list.append(new_cmd)

            cmd_list.append(tmp_cmd_list)

        return cmd_list
