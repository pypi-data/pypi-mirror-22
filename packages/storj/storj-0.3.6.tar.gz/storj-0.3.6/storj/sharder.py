import math
import os


class ShardingTools():

    def __init__(self):
        self.MAX_SHARD_SIZE = 4294967296  # 4Gb
        self.SHARD_MULTIPLES_BACK = 4

    def get_optimal_shard_parametrs(self, file_size):
        shard_parameters = {}
        accumulator = 0
        shard_size = None
        while (shard_size is None):
            shard_size = self.determine_shard_size(file_size, accumulator)
            accumulator += 1
        shard_parameters["shard_size"] = str(shard_size)
        shard_parameters["shard_count"] = math.ceil(file_size / shard_size)
        shard_parameters["file_size"] = file_size
        return shard_parameters

    def determine_shard_size(self, file_size, accumulator):

        # Based on <https://github.com/aleitner/shard-size-calculator
        # /blob/master/src/shard_size.c>

        hops = 0

        if (file_size <= 0):
            return 0
            # if accumulator != True:
            # accumulator  = 0
        print accumulator

        # Determine hops back by accumulator
        if ((accumulator - self.SHARD_MULTIPLES_BACK) < 0):
            hops = 0
        else:
            hops = accumulator - self.SHARD_MULTIPLES_BACK

        # accumulator = 10
        byte_multiple = self.shard_size(accumulator)

        check = file_size / byte_multiple
        # print check
        if (check > 0 and check <= 1):
            while (hops > 0 and self.shard_size(hops) > self.MAX_SHARD_SIZE):
                if hops - 1 <= 0:
                    hops = 0
                else:
                    hops = hops - 1
            return self.shard_size(hops)

        # Maximum of 2 ^ 41 * 8 * 1024 * 1024
        if (accumulator > 41):
            return 0

            # return self.determine_shard_size(file_size, ++accumulator)

    def shard_size(self, hops):
        return (8 * (1024 * 1024)) * pow(2, hops)

    def sort_index(self, f1, f2):

        index1 = f1.rfind('-')
        index2 = f2.rfind('-')

        if index1 != -1 and index2 != -1:
            i1 = int(f1[index1:len(f1)])
            i2 = int(f2[index2:len(f2)])
            return i2 - i1

    def join_shards(self, shards_filepath, pattern, destination_file_path):
        # Based on <http://code.activestate.com/recipes/224800
        # -simple-file-splittercombiner-module/>
        import re

        print 'Creating file ' + destination_file_path

        bname = os.path.split(destination_file_path)[1]
        bname_input = os.path.split(shards_filepath)[1]
        bname2_input = bname_input

        input_directory = os.path.split(shards_filepath)[0]
        output_directory = os.path.split(destination_file_path)[0]

        # bugfix: if file contains characters like +,.,[]
        # properly escape them, otherwise re will fail to match.
        for a, b in zip(['+', '.', '[', ']', '$', '(', ')'],
                        ['\+', '\.', '\[', '\]', '\$', '\(', '\)']):
            bname2 = bname2_input.replace(a, b)

        chunkre = re.compile(bname2_input + '-' + '[0-9]+')

        chunkfiles = []
        for f in os.listdir(str(input_directory)):
            if chunkre.match(f):
                chunkfiles.append(f)

        print 'Number of chunks ', len(chunkfiles)
        chunkfiles.sort(self.sort_index)
        print chunkfiles
        data = ''
        for f in chunkfiles:
            try:
                print 'Appending chunk', os.path.join(input_directory, f)
                data += open(
                    os.path.join(input_directory, str(f)), 'rb').read()
            except (OSError, IOError, EOFError) as e:
                print e
                continue

        try:
            print "Write joined file in " + output_directory
            with open(os.path.join(output_directory, bname), 'wb') as f:
                f.write(data)
        except (OSError, IOError, EOFError) as e:
            raise ShardingException(str(e))

        print 'Wrote file', bname
        return 1


class ShardingException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
