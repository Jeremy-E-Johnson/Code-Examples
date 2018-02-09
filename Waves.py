# takes Function tuple IC
# tuple of Function LBC, Function RBC
# tuple of Boolean Dir=true Nue=false left and right
# tuple interval
# contains: s stub/scheme stubs


class PDEproblem():
    def __init__(self, initialConditions, bc, dirc, interval):
        self.xmin, self.xmax = interval
        self.ic = initialConditions
        self.lbc, self.rbc = bc
        self.ldirc, self.rdirc = dirc

    def getS():
        return 0

    def forwardScheme(dx, dt, x, t):
        return 0

    def backwardScheme(dx, dt, x, t):
        return 0

    def centerScheme(dx, dt, x, t):
        return 0

    def crankNicolson(dx, dt, x, t):
        return 0


class Wave(PDEproblem):
    def __init__(self, initialConditions, bc, dirc, interval):
        super().__init__(initialConditions, bc, dirc, interval)
        self.uic, self.utic = self.ic

    def centerScheme(self, dx, dt, x, t, c):
        # Calculate s and hold it
        s = ((c * dt)**2) / ((dx)**2)

        # Find number of finite values to hold
        intervalSize = (self.xmax - self.xmin)
        intervals = int(intervalSize / dx)

        # Initialize composed arrays for uvalues (time,space)
        uvalues = [0 for x in range(int(t / dt) + 1)]
        for i in range(int(t / dt) + 1):
            uvalues[i] = [0 for x in range(intervals + 3)]

        # Initialize u values for t = 0
        for i in range(intervals + 1):
            uvalues[0][i + 1] = self.uic((i * dx) + self.xmin)

        # Initialize Dirchlet end points (with zero ghosts), or Neuman ghost points
        if(self.ldirc):
            uvalues[0][1] = self.lbc(0)
            uvalues[0][0] = 0
        else:
            uvalues[0][0] = uvalues[0][1] - (2 * dx * self.lbc(0))
        if(self.rdirc):
            uvalues[0][intervals + 1] = self.rbc(0)
            uvalues[0][intervals + 2] = 0
        else:
            uvalues[0][intervals + 2] = uvalues[0][intervals] + (2 * dx * self.rbc(0))

        # Initialize u values for t = 1
        # Start for values on interiors
        for i in range(1, intervals):
            uvalues[1][i + 1] = ((s / 2) * (self.uic((i + 1) * dx) + self.uic((i - 1) * dx))) + ((1 - s) * self.uic(i * dx)) + (self.utic(i * dx) * dt)

        # Do values on boundry for t = 1 by boundry condidions.
        if(self.ldirc):
            uvalues[1][1] = self.lbc(dt)
            uvalues[1][0] = 0
        else:
            uvalues[1][1] = (s / 2)(self.uic(dx) + self.uic(dx) - (2 * dx * self.lbc(dt))) + (1 - s)(self.uic(0)) + (self.utic(0) * dt)
            uvalues[1][0] = uvalues[1][2] - (2 * dx * self.lbc(dt))
        if(self.rdirc):
            uvalues[1][intervals + 1] = self.rbc(dt)
            uvalues[1][intervals + 2] = 0
        else:
            uvalues[1][intervals + 1] = ((s / 2) * (self.uic(dx * (intervals - 1)) + self.uic(dx + (intervals - 1)) + (2 * dx * self.rbc(dt)))) + ((1 - s) * (self.uic(intervals * dx))) + (self.utic(intervals * dx) * dt)
            uvalues[1][intervals + 2] = uvalues[1][intervals] + (2 * dx * self.rbc(dt))

        # Now, hopefully, we can start stepping forward.
        # Calculate number of steps to get to desired point.
        stepsInTime = int(t/dt)

        # Stop if we already got there.
        if(stepsInTime < 2):
            return uvalues[stepsInTime][(int((x - self.xmin) / dx)) + 1]
        # Step forward if we havent
        for i in range(2, stepsInTime + 1):
            # Calculate interior
            for k in range(1, intervals + 1):
                uvalues[i][k + 1] = (s * (uvalues[i - 1][k + 2] + uvalues[i - 1][k])) + (2 * (1 - s) * uvalues[i - 1][k + 1]) - uvalues[i - 2][k + 1]
            # Do boundries
            if(self.ldirc):
                uvalues[i][1] = self.lbc(dt * i)
                uvalues[i][0] = 0
            else:
                #uvalues[i][1] = (s / 2)(self.uic(dx) + self.uic(dx) - (2 * dx * self.lbc(dt))) + (1 - s)(self.uic(0)) + (self.utic(0) * dt)
                uvalues[i][0] = uvalues[i][2] - (2 * dx * self.lbc(dt * i))
            if(self.rdirc):
                uvalues[i][intervals + 1] = self.rbc(dt * i)
                uvalues[i][intervals + 2] = 0
            else:
                #uvalues[i][intervals + 1] = ((s / 2) * (self.uic(dx * (intervals - 1)) + self.uic(dx + (intervals - 1)) + (2 * dx * self.rbc(dt)))) + ((1 - s) * (self.uic(intervals * dx))) + (self.utic(intervals * dx) * dt)
                uvalues[i][intervals + 2] = uvalues[i][intervals] + (2 * dx * self.rbc(dt * i))

        for list in uvalues:
            print(list[1:intervals + 2])

        return uvalues[stepsInTime][(int((x - self.xmin) / dx)) + 1]


class Diffusion(PDEproblem):
    def __init__(self, initialConditions, bc, dirc, interval):
        super().__init__(initialConditions, bc, dirc, interval)
        self.uic = self.ic

    def centerScheme(self, dx, dt, x, t, k):
        # Compute s and hold it
        s = (dt / ((dx)**2))

        # Find number of finite values to hold
        intervalSize = (self.xmax - self.xmin)
        intervals = int(intervalSize / dx)

        # Initialize composed arrays for uvalues (time,space)
        uvalues = [0 for x in range(int(t / dt) + 1)]
        for i in range(int(t / dt) + 1):
            uvalues[i] = [0 for x in range(intervals + 3)]

        # Initialize u values for t = 0
        for i in range(intervals + 1):
            uvalues[0][i + 1] = self.uic((i * dx) + self.xmin)

        # Initialize Dirchlet end points (with zero ghosts), or Neuman ghost points
        if(self.ldirc):
            uvalues[0][1] = self.lbc(0)
            uvalues[0][0] = 0
        else:
            uvalues[0][0] = uvalues[0][1] - (2 * dx * self.lbc(0))
        if(self.rdirc):
            uvalues[0][intervals + 1] = self.rbc(0)
            uvalues[0][intervals + 2] = 0
        else:
            uvalues[0][intervals + 2] = uvalues[0][intervals] + (2 * dx * self.rbc(0))

        # Now, hopefully, we can start stepping forward.
        # Calculate number of steps to get to desired point.
        stepsInTime = int(t/dt)

        # Stop if we already got there.
        if(stepsInTime == 0):
            return uvalues[0][(int((x - self.xmin) / dx)) + 1]

        # Step forward if we havent
        for i in range(1, stepsInTime + 1):
            # Calculate interior
            for k in range(1, intervals + 1):
                uvalues[i][k + 1] = (s * (uvalues[i - 1][k + 2] + uvalues[i - 1][k])) + ((1 - (2 * s)) * (uvalues[i - 1][k + 1]))
            # Do boundries
            if(self.ldirc):
                uvalues[i][1] = self.lbc(dt * i)
                uvalues[i][0] = 0
            else:
                #uvalues[i][1] = (s / 2)(self.uic(dx) + self.uic(dx) - (2 * dx * self.lbc(dt))) + (1 - s)(self.uic(0)) + (self.utic(0) * dt)
                uvalues[i][0] = uvalues[i][2] - (2 * dx * self.lbc(dt * i))
            if(self.rdirc):
                uvalues[i][intervals + 1] = self.rbc(dt * i)
                uvalues[i][intervals + 2] = 0
            else:
                #uvalues[i][intervals + 1] = ((s / 2) * (self.uic(dx * (intervals - 1)) + self.uic(dx + (intervals - 1)) + (2 * dx * self.rbc(dt)))) + ((1 - s) * (self.uic(intervals * dx))) + (self.utic(intervals * dx) * dt)
                uvalues[i][intervals + 2] = uvalues[i][intervals] + (2 * dx * self.rbc(dt * i))

        for list in uvalues:
            print(list[1:intervals + 2])

        return uvalues[stepsInTime][(int((x - self.xmin) / dx)) + 1]


def u(x):
    return 25 - x**2

def ut(x):
    return 0

def boundryConditions(x):
    return 0


def main():
    problem = Wave((u, ut), (boundryConditions, boundryConditions), (True, False), {0, 5})
    print(problem.centerScheme(1.0, .5, 3, 50, 1.0))

    problem2 = Diffusion(u, (boundryConditions, boundryConditions), (True, True), {0, 5})
    #print(problem2.centerScheme(1, .5, 3, 50, 1))

main();