import markplates

def test_condense_ranges():
    for item in dir(markplates):
        print(item)
    counting_lines = [str(x+1) + "\n" for x in range(13)]
    # output_lines = markPlates.condense_ranges(counting_lines, None)
    # ranges = ["2", 3, "5-6", "9-$", ]
    # ranges = ["9-$", "2", "5-6", 3, "5-6", "9-$", ]
    ranges = [2, ]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert '2\n' in output_lines
    assert '3\n' not in output_lines

    # print(output_lines)
    # output = "".join(output_lines)
    # print(output)
