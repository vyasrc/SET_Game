from itertools import combinations
import time


class Attributes:
    """Attributes for one card."""
    def __init__(self, color, symbol, shading, number):
        self.color = color
        self.symbol = symbol
        self.shading = shading
        self.number = number


class SET:
    """A collection of SET cards."""
    def __init__(self):
        self.objects = []
        self.sets = []
        self.converted_sets = []

    @staticmethod
    def input_to_attributes(input_string):
        """Convert the input string from i/o to a Attributes class object properties and return them."""

        color = input_string.split(' ')[0]
        number = len(input_string.split(' ')[1])
        if input_string.split(' ')[1][0] in ['@', '$', '#']:
            shading = 'symbol-case'
        elif input_string.split(' ')[1][0] in ['A', 'S', 'H']:
            shading = 'upper-case'
        elif input_string.split(' ')[1][0] in ['a', 's', 'h']:
            shading = 'lower-case'
        else:
            raise Exception("Invalid Input")

        if input_string.split(' ')[1][0] in ['h', 'H', '#']:
            symbol = 'H'
        elif input_string.split(' ')[1][0] in ['s', 'S', '$']:
            symbol = 'S'
        elif input_string.split(' ')[1][0] in ['a', 'A', '@']:
            symbol = 'A'
        else:
            raise Exception("Invalid Input")

        return color, symbol, shading, number

    def assign(self, input_string):
        """Initialize a Attributes Class Object and append it to the objects list."""

        color, symbol, shading, number = self.input_to_attributes(input_string)

        self.objects.append(Attributes(color, symbol, shading, number))

    def find_sets(self):
        """Find all possible SETs of three cards in the input. A set of three cards forms a SET if (and only if), for
        each of the four attributes, the three cards either all have the same attribute value or all have different
        values."""

        for comb in combinations(self.objects, 3):

            if len({comb[0].color, comb[1].color, comb[2].color}) == 2:
                continue
            elif len({comb[0].symbol, comb[1].symbol, comb[2].symbol}) == 2:
                continue
            elif len({comb[0].shading, comb[1].shading, comb[2].shading}) == 2:
                continue
            elif len({comb[0].number, comb[1].number, comb[2].number}) == 2:
                continue
            else:
                self.sets.append(comb)

        return len(self.sets)

    @staticmethod
    def attributes_to_output(s):
        """Convert a Attributes Class Object into a string value and return it."""

        ans = s.color + ' '
        if s.symbol == 'H' and s.shading == 'symbol-case':
            ans += '#' * s.number
        elif s.symbol == 'H' and s.shading == 'upper-case':
            ans += 'H' * s.number
        elif s.symbol == 'H' and s.shading == 'lower-case':
            ans += 'h' * s.number
        elif s.symbol == 'A' and s.shading == 'symbol-case':
            ans += '@' * s.number
        elif s.symbol == 'A' and s.shading == 'upper-case':
            ans += 'A' * s.number
        elif s.symbol == 'A' and s.shading == 'lower-case':
            ans += 'a' * s.number
        elif s.symbol == 'S' and s.shading == 'symbol-case':
            ans += '$' * s.number
        elif s.symbol == 'S' and s.shading == 'upper-case':
            ans += 'S' * s.number
        elif s.symbol == 'S' and s.shading == 'lower-case':
            ans += 's' * s.number

        return ans

    def convert(self):
        """Convert all possible SET cards found into a string format."""

        for s in self.sets:
            self.converted_sets.append([self.attributes_to_output(s[0]), self.attributes_to_output(s[1]),
                                        self.attributes_to_output(s[2])])

    def graph_sets(self, graph):
        """Find the maximum independent set in the graph which is equivalent to the maximum number of disjoint SETs
        in the input."""

        if len(graph) == 0:
            return []

        if len(graph) == 1:
            return [list(graph.keys())[0]]

        v_current = list(graph.keys())[0]

        graph2 = dict(graph)
        del graph2[v_current]

        res1 = self.graph_sets(graph2)

        for v in graph[v_current]:
            if v in graph2:
                del graph2[v]

        res2 = [v_current] + self.graph_sets(graph2)

        if len(res1) > len(res2):
            return res1

        return res2

    def find_disjoint_sets(self):
        """Find the maximum number of disjoint SETs in the input. Create a graph so that lists are vertices and two
        vertices are connected if they are not disjoint."""

        graph = dict([])

        for comb in combinations(self.converted_sets, 2):
            if len(set([y for x in comb for y in x])) < 6:
                v1 = self.converted_sets.index(comb[0])
                v2 = self.converted_sets.index(comb[1])

                if v1 not in graph:
                    graph[v1] = []
                if v2 not in graph:
                    graph[v2] = []

                graph[v1].append(v2)
                graph[v2].append(v1)

        result = self.graph_sets(graph)
        print(len(result))
        print('\n')
        self.display(result)

    def display(self, result):
        """Display the cards forming a largest collection of disjoint SETs."""

        for j in result:
            for item in self.converted_sets[j]:
                print(item)
            print('\n')


if __name__ == '__main__':
    n = int(input())
    obj = SET()
    for i in range(n):
        obj.assign(input())
    start = time.time()
    print(obj.find_sets())
    obj.convert()
    obj.find_disjoint_sets()
    end = time.time()
    print(f'The output was generated in {end - start} seconds')