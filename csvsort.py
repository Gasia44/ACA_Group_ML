from argparse import ArgumentParser
import sys
import operator

from utils import report_error, report_wrong_number_of_columns, InputError

DESCRIPTION = 'csvsort - prints cvs file sorted by given columns'
EXAMPLES = 'example: cat file.txt | csvsort -k "string1-string2" | less -SR'


def print_row(row, column_widths, output_stream, careful, quiet):
    """
    Prints a row in human-readable format taking column widths into account

    :param row: row represented as a list of columns
    :param column_widths: a list of column list widths to be used for pretty printing
    :param output_stream: a stream to pretty print the row
    """
    if (len(column_widths) != len(row)):
        report_wrong_number_of_columns(row, careful, quiet)

    output_line = '|'
    for i, column in enumerate(row):
        width = column_widths[i] if i < len(column_widths) else 0
        output_line += ' ' + column + ' ' * (width - len(column) + 1) + '|'
    output_line += '\n'
    output_stream.write(output_line)

def criteria(keys,columns):
    crit = []
    crit_n=[]
    if '-' in keys:
        col_select = keys.split('-')
        select = False
        i = 0
        for col in columns:
            if col == col_select[0].replace(' ',''):
                select = True

            if select:
                crit.append(col.replace(' ',''))
                crit_n.append(i)
            i+=1
            if col == col_select[1].replace(' ',''):
                break

    elif ',' in keys:
        col_select = keys.split(',')
        for col in col_select:
            crit.append(col.replace(' ',''))


    else:
        crit.append(keys.replace(' ',''))

    return crit, crit_n

def main(args):
    input_stream = sys.stdin
    output_stream = sys.stdout
    try:
        args = parse_args()
        input_stream = open(args.file, 'r') if args.file else sys.stdin
        output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout
        columns = input_stream.readline().strip().split(args.separator)

        select=criteria(args.keys,columns)


        first_rows=[]
        i=0
        for line in input_stream:
            i+=1
            row = line.strip().split(args.separator)
            first_rows.append(row)
            # Read no more than lines_number first lines
            if i== args.max_rows:
                break


        if args.numeric:
            print("barev")
            for i in select[1]:
                for j in range(len(first_rows)):
                    if type(first_rows[j][i])==str:
                        first_rows[j][i]=float(first_rows[j][i])

            first_rows=sorted(first_rows, key=operator.itemgetter(*select[1]), reverse=args.descending)

            for i in select[1]:
                for j in range(len(first_rows)):
                    if type(first_rows[j][i])!=str:
                        first_rows[j][i]=str(first_rows[j][i])
        else:
            first_rows=sorted(first_rows, key=operator.itemgetter(*select[1]), reverse=args.descending)


        first_rows.insert(0,columns)

        column_widths = [max([len(column) for column in [row[i] for row in first_rows]]) for i in range(len(columns))]


        for row in first_rows:
            print_row(row, column_widths, output_stream, args.careful, args.quiet)

    except FileNotFoundError:
        report_error("File {} doen't exist".format(args.file))
    except InputError as e:
        report_error(e.message + '. Row: ' + str(e.expression))
    except KeyboardInterrupt:
        pass
    except BrokenPipeError:
        # The following line prevents python to inform you about the broken pipe
        sys.stderr.close()
    except ValueError:
        report_error("Maybe you have an element of type 'str' in sorting column, which couldn't be converted to numeric format")
    except Exception as e:
        report_error('Caught unknown exception. Please report to developers: {}'.format(e))
    finally:
        if input_stream and input_stream != sys.stdin:
            input_stream.close()
        if output_stream:
            output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-m', '--max_rows', type=int, help="Don't load to memory more than MAX_ROWS rows at a time. This option is crucial if you have to deal with huge csv files. Default value is 0 that meanse that this will sort file in memory",
                        default=0)
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('-q', '--quiet', help="Don't print information regarding errors", action='store_true')
    parser.add_argument('-k', '--keys', type=str, help="Specify the list of keys (comma separated) to sort on. Field names or field numbers can be used. Dash can be used to specify fields ranges. Range 'F1-F2' stands for all fields between F1 and F2. Range '-F2' stands for all fields up to F2. Range 'F1-' stands for all fields from F1 til the end.", default='1')
    parser.add_argument('--descending', help='If provided, perform descending sort instead of ascending', action='store_true')
    parser.add_argument('--numeric', help='If provided, keys will be interpreted as numbers. Otherwise - as strings', action='store_true')

    parser.add_argument('--careful', help='Stop if input contains an incorrect row', action='store_true')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    main(parse_args())
