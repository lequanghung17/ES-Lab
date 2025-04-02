
from pysat.solvers import Glucose3
import math
class SCLEncoder():
    def __init__(self, clause_container, var_handler):
        super().__init__(clause_container, var_handler)
        self.cc = clause_container
        self.vh = var_handler
        # Dictionary to store auxiliary variables: key is (first, last) pair.
        self.aux_vars = {}

    def get_aux_var(self, first, last):
        if (first, last) in self.aux_vars:
            return self.aux_vars[(first, last)]
        if first == last:
            return first
        new_aux_var = self.vh.get_new_var()
        self.aux_vars[(first, last)] = new_aux_var
        return new_aux_var

    def encode_and_solve_ladder_amo(self, n, w, initCondLength, initCond):
        # The parameters initCondLength and initCond are not used.
        total_windows = math.ceil(n / w)
        for gw in range(total_windows):
            self.encode_window(gw, n, w)
        for gw in range(total_windows - 1):
            self.glue_window(gw, n, w)

    def encode_window(self, window, n, w):
        total_windows = math.ceil(n / w)
        if window == 0:
            # First window (only lower part)
            lastVar = window * w + w

            # Formula 7
            for i in range(2, w):
                var = window * w + w + 1 - i
                self.cc.add_clause([-var, self.get_aux_var(var, lastVar)])

            # Formula 8
            for i in range(2, w):
                var = window * w + w + 1 - i
                self.cc.add_clause([-self.get_aux_var(var + 1, lastVar),
                                      self.get_aux_var(var, lastVar)])

            # Formula 9
            for i in range(2, w):
                var = window * w + w + 1 - i
                sub = self.get_aux_var(var + 1, lastVar)
                main = self.get_aux_var(var, lastVar)
                self.cc.add_clause([var, sub, -main])

            # Formula 10
            for i in range(2, w + 1):
                var = window * w + w + 1 - i
                self.cc.add_clause([-var, -self.get_aux_var(var + 1, lastVar)])

        elif window == total_windows - 1:
            # Last window (only upper part, may have width lower than w)
            firstVar = window * w + 1

            if (window + 1) * w > n:
                real_w = n % w  # actual width < w
                # Formula 7 (upper part)
                for i in range(2, real_w + 1):
                    reverse_var = window * w + i
                    self.cc.add_clause([-reverse_var, self.get_aux_var(firstVar, reverse_var)])

                # Formula 8
                for i in range(2, real_w + 1):
                    reverse_var = window * w + i - 1
                    self.cc.add_clause([-self.get_aux_var(firstVar, reverse_var),
                                          self.get_aux_var(firstVar, reverse_var + 1)])

                # Formula 9
                for i in range(2, real_w + 1):
                    var = window * w + i
                    sub = self.get_aux_var(firstVar, var - 1)
                    main = self.get_aux_var(firstVar, var)
                    self.cc.add_clause([var, sub, -main])

                # Formula 10
                for i in range(2, real_w + 1):
                    reverse_var = window * w + i
                    self.cc.add_clause([-reverse_var, -self.get_aux_var(firstVar, reverse_var - 1)])
            else:
                # Upper part (full width w)
                # Formula 7
                for i in range(2, w):
                    reverse_var = window * w + i
                    self.cc.add_clause([-reverse_var, self.get_aux_var(firstVar, reverse_var)])

                # Formula 8
                for i in range(2, w):
                    reverse_var = window * w + i - 1
                    self.cc.add_clause([-self.get_aux_var(firstVar, reverse_var),
                                          self.get_aux_var(firstVar, reverse_var + 1)])

                # Formula 9
                for i in range(2, w):
                    var = window * w + i
                    sub = self.get_aux_var(firstVar, var - 1)
                    main = self.get_aux_var(firstVar, var)
                    self.cc.add_clause([var, sub, -main])

                # Formula 10
                for i in range(2, w + 1):
                    reverse_var = window * w + i
                    self.cc.add_clause([-reverse_var, -self.get_aux_var(firstVar, reverse_var - 1)])

        else:
            # Middle windows (both upper and lower parts, full width w)
            firstVar = window * w + 1

            # Upper part
            # Formula 7
            for i in range(2, w):
                reverse_var = window * w + i
                self.cc.add_clause([-reverse_var, self.get_aux_var(firstVar, reverse_var)])

            # Formula 8
            for i in range(2, w):
                reverse_var = window * w + i - 1
                self.cc.add_clause([-self.get_aux_var(firstVar, reverse_var),
                                      self.get_aux_var(firstVar, reverse_var + 1)])

            # Formula 9
            for i in range(2, w):
                var = window * w + i
                sub = self.get_aux_var(firstVar, var - 1)
                main = self.get_aux_var(firstVar, var)
                self.cc.add_clause([var, sub, -main])

            # Formula 10
            for i in range(2, w + 1):
                reverse_var = window * w + i
                self.cc.add_clause([-reverse_var, -self.get_aux_var(firstVar, reverse_var - 1)])

            # Lower part
            lastVar = window * w + w

            # Formula 7
            for i in range(2, w):
                var = window * w + w + 1 - i
                self.cc.add_clause([-var, self.get_aux_var(var, lastVar)])

            # Formula 8
            for i in range(2, w):
                var = window * w + w + 1 - i
                self.cc.add_clause([-self.get_aux_var(var + 1, lastVar),
                                      self.get_aux_var(var, lastVar)])

            # Formula 9
            for i in range(2, w):
                var = window * w + w + 1 - i
                sub = self.get_aux_var(var + 1, lastVar)
                main = self.get_aux_var(var, lastVar)
                self.cc.add_clause([var, sub, -main])

            # The following Formula 10 is commented out (disabled)
            # for i in range(2, w + 1):
            #     var = window * w + w + 1 - i
            #     self.cc.add_clause([-var, -self.get_aux_var(var + 1, lastVar)])

    def glue_window(self, window, n, w):
        if (window + 2) * w > n:
            real_w = n % w
            for i in range(1, real_w + 1):
                first_reverse_var = (window + 1) * w + 1
                last_var = window * w + w
                reverse_var = (window + 1) * w + i
                var = window * w + i + 1
                self.cc.add_clause([-self.get_aux_var(var, last_var),
                                      -self.get_aux_var(first_reverse_var, reverse_var)])
        else:
            for i in range(1, w):
                first_reverse_var = (window + 1) * w + 1
                last_var = window * w + w
                reverse_var = (window + 1) * w + i
                var = window * w + i + 1
                self.cc.add_clause([-self.get_aux_var(var, last_var),
                                      -self.get_aux_var(first_reverse_var, reverse_var)])
