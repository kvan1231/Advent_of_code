# https://adventofcode.com/2022/day/7


class Commands():
    """
    This class will contain a list of strings that represent terminal inputs
    """

    def __init__(self, file_name: str = "test.txt") -> list:
        """
        This function reads in the text file that contains the commands

        Parameters
        ----------
        file_name: str
            The name of the file we're going to read in
        """

        # read in the data
        with open(file_name) as f:
            raw_data = f.read().strip().split('\n')

        # store the commands
        self.cmd = raw_data

    def storage_calc(self, max_size: int = 100000) -> int:
        """
        This function calculates the total storage requirement of the files
        that are smaller than the max_size

        Parameters
        ----------
        max_size: float
            The maximum size of the files we're interested in
        """

        command = self.cmd

        # create a dictionary relating file name to file size
        files = {}

        # track the current working directory
        cwd = []

        # track the directories in a set as we only need them once
        dirs = set()

        # loop through the commands
        for cmd in command:
            # if the command starts with a $ then we have either $ ls or $ cd
            # ignore the $ ls ones and only focus on $ cd
            if cmd.startswith("$"):
                if cmd.startswith("$ cd"):
                    # scrape the directory name
                    dir_name = cmd[5:]

                    # if the directory name is .. then change current directory
                    if dir_name == "..":
                        # if we're somewhere not home
                        if len(cwd) > 0:
                            cwd.pop(-1)
                    elif dir_name == "/":
                        # we've returned home
                        cwd = []
                    else:
                        cwd.extend(dir_name.split("/"))


            # if the command doesnt start with $ then we are reading the output
            # of an ls command which outputs the size of the files and various
            # directories contained
            else:
                info, name =  cmd.split(" ")
                if info != "dir":
                    size = int(info)
                    files["/".join(cwd + [name])] = size
            dirs.add("/".join(cwd))

        # now that we have all of the sizes associated with files we need
        # to combine them into directories

        dir_sizes = {}
        # loop through directories
        for directory in dirs:

            # initialize
            dir_size = 0

            # loop through files
            for file in files:
                if file.startswith(directory):

                    # add size
                    dir_size += files[file]
            # attach the size to dictonary
            dir_sizes[directory] = dir_size

        # find the number of directories smaller than our max value
        largest_dirs = {
            key:value for (key, value) in dir_sizes.items() if value < max_size
            }

        dir_count = sum(largest_dirs.values())

        # find the smallest directory that when deleted would free up 30000000
        smallest_dirs = {
            key:value for (key, value) in dir_sizes.items() if
            70000000 - dir_sizes[""] + value >= 30000000
        }
        smallest_dir_size = min(smallest_dirs.values())

        return dir_count, smallest_dir_size


def solution():
    pt1_sol, pt2_sol = Commands('input.txt').storage_calc()

    print("part 1 sol:", pt1_sol)
    print("part 2 sol:", pt2_sol)
