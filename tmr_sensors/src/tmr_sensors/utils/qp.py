""""
% Minimize 0.5*x'*H*x + x'*g  s.t. lower<=x<=upper
%
%  inputs:
%     H            - positive definite matrix   (n * n)
%     g            - bias vector                (n)
%     lower        - lower bounds               (n)
%     upper        - upper bounds               (n)
%
%   optional inputs:
%     x0           - initial state              (n)
%     options      - see below                  (7)
%
%  outputs:
%     x            - solution                   (n)
%     result       - result type (roughly, higher is better, see below)
%     Hfree        - subspace cholesky factor   (n_free * n_free)
%     free         - set of free dimensions     (n)
% This is code ported to Python, originally written by Y.Tassa in matlab
"""

import numpy as np
np.random.seed(0)

class boxQP():
    def __init__(self, H, g, lower, upper, x0, options=None):
        self.n        = H.shape[0]
        self.clamped  = np.matrix(np.zeros((self.n,1), dtype=bool))
        self.free     = np.matrix(np.ones((self.n,1), dtype=bool))
        self.H        = H
        self.g        = g
        self.lower    = lower
        self.upper    = upper
        self.oldvalue = 0
        self.result   = 0
        self.gnorm    = 0
        self.nfactor  = 0
        self.trace    = []
        self.Hfree    = np.matrix(np.zeros((self.n,self.n)))
        self.clamp    = self.clampTool
        if options != None:
            self.maxIter        = options[0]     # maximum number of iterations
            self.minGrad        = options[1]     # minimum norm of non-fixed gradient
            self.minRelImprove  = options[2]     # minimum relative improvement
            self.stepDec        = options[3]     # factor for decreasing stepsize
            self.minStep        = options[4]     # minimal stepsize for linesearch
            self.Armijo         = options[5]     # Armijo parameter (fraction of linear improvement required)
            self.verbose        = options[6]
        else:
            self.maxIter        = 100;       
            self.minGrad        = 1e-8;     
            self.minRelImprove  = 1e-8;      
            self.stepDec        = 0.6;      
            self.minStep        = 1e-22;     
            self.Armijo         = 0.1;       
            self.verbose        = 1
        self.x = self.initVal(x0,lower,upper)
        self.out = 5

    def clampTool(self,x):
        return np.maximum(lower,np.minimum(upper, x))

    def initVal(self, x0, lower, upper):
        if((x0 is not None)&(len(x0) == n)):
            x = self.clamp(x0)
        else:
            LU = np.concatenate((lower, upper))
            LU[~np.isfinite(LU)] = float('nan')
            x = np.nanmean(LU,2) #takes average ingoring nan values
        return np.matrix(x)

    def QPsolve(self):
        x        = self.x
        result   = self.result
        clamped  = self.clamped
        free     = self.free
        xfnl     = []
        xcfnl    = []
        valfnl   = []
        srchfnl  = []
        clmpfnl  = []
        nfctrfnl = []
        Hfree    =  self.Hfree

        x[~np.isfinite(x)] = 0
        #print x
        value    = x.T*g + 0.5*x.T*H*x; # initial objective value
        #print value
        if self.verbose:
            print '==========\nStarting box-QP, dimension {}, initial value: {}\n'.format(n, value)
            
        for itr in range(self.maxIter): # main loop
            print "Iteration \t", itr
            if result != 0:
                break
            if((itr > 0) & ((self.oldvalue - value) < self.minRelImprove*np.absolute(self.oldvalue))):  # check relative improvement
                result = 4
                break
            self.oldvalue = value
            #print self.oldvalue
            # get gradient
            grad  = g + H*x
            #print grad
            # find clamped dimensions
            old_clamped                     = clamped
            clamped                         = np.matrix(np.zeros((self.n,1), dtype=bool))
            #print x.shape
            clamped[(x == lower)&(grad>0)]  = True
            clamped[(x == upper)&(grad<0)]  = True
            free                            = ~clamped
            #print free
            # check for all clamped
            if np.all(clamped):
                result = 6
                break  
            # factorize if clamped has changed
            if itr == 0:
                factorize    = True
            else:
                factorize    = np.any(old_clamped!= clamped)      
            
            freeD = np.matrix(np.nonzero(free.astype(int)))
            freeD = freeD[0].T #converting to indexes for selecting from matrices
            clampD = np.matrix(np.nonzero(clamped.astype(int)))
            clampD = clampD[0].T

            if factorize:
                try:
                    Hfree  = np.linalg.cholesky(H[freeD.T,freeD].T)
                except np.linalg.LinAlgError:
                    result = -1
                    break
                #Hfree =  Hfree.T
                #print Hfree
                self.nfactor  +=  1
            # check gradient norm
            self.gnorm  = np.linalg.norm(grad[freeD].flatten().T)
            #print self.gnorm
            if self.gnorm < self.minGrad:
                result = 5
                # print "here"
                break
            # get search direction
            grad_clamped   = g  + H*(np.multiply(x,clamped.astype(int)))
            #print grad_clamped
            search         = np.matrix(np.zeros((n,1)))
            temp   = -np.linalg.inv(Hfree)*(np.linalg.inv(Hfree.T)*grad_clamped[freeD].flatten().T) - x[freeD].flatten().T
            for i in range(freeD.shape[0]):
                search[freeD[i]] = temp[i]
            #print search
            # check for descent direction
            sdotg          =np.sum(np.multiply(search, grad))
            print sdotg
            if sdotg >= 0: # (should not happen)
                print "here"
                break      
            # armijo linesearch
            step  = 1
            nstep = 0
            xc    = self.clamp(x+step*search)
            vc    = xc.T*g + 0.5*xc.T*H*xc
            #print vc
            while ((vc - self.oldvalue)/(step*sdotg)) < self.Armijo:
                step  = step*self.stepDec
                nstep += 1
                xc    = self.clamp(x+step*search)
                vc    = xc.T*g + 0.5*xc.T*H*xc
                if step < self.minStep:
                    result = 2
            #print xc
            if self.verbose:
                print 'itr {}  value {} |g| {}  reduction {}  linesearch {}^{}  n_clamped {}\n'.\
                format(itr, vc, self.gnorm, self.oldvalue-vc, self.stepDec, nstep, np.sum(clamped.astype(int)))
 
            if self.out>4:
                xfnl.append(x) 
                xcfnl.append(xc) 
                valfnl.append(value) 
                srchfnl.append(search)
                clmpfnl.append(clamped)
                nfctrfnl.append(self.nfactor)
            # accept candidate
            x     = xc
            value = vc


        if itr>=self.maxIter:
            result = 1

        results =   ['Hessian is not positive definite',            # result = -1
                    'No descent direction found',                   # result = 0    SHOULD NOT OCCUR
                    'Maximum main iterations exceeded',             # result = 1
                    'Maximum line-search iterations exceeded',      # result = 2
                    'No bounds, returning Newton point',            # result = 3
                    'Improvement smaller than tolerance',           # result = 4
                    'Gradient norm smaller than tolerance',         # result = 5
                    'All dimensions are clamped'];                  # result = 6
        
        self.trace.append(xfnl)
        self.trace.append(xcfnl)
        self.trace.append(valfnl)
        self.trace.append(srchfnl)
        self.trace.append(clmpfnl)
        self.trace.append(nfctrfnl)
        if self.verbose:
             print "RESULT: {} \niterations {}  gradient {} final value {}  factorizations {}\n".\
             format(results[result+1], itr+1, self.gnorm, value, self.nfactor)
        
        return x,results[result+1],Hfree,free, self.trace
            
if __name__=="__main__":
    options = None #[100, 1e-1, 1e-1, 0.6, 1e-1, 0.1, 1] # defaults with detailed printing
    n       = 500
    g       = np.matrix(np.random.randn(n,1))
    H       = np.matrix(np.random.randn(n,n))
    H       = H*H.T
    lower   = np.matrix(-1000000*np.ones((n,1)))
    upper   = np.matrix(1000000*np.ones((n,1)))
    x0      = np.matrix(np.random.randn(n,1))
    box = boxQP(H, g, lower, upper, x0, options) 
    x,result, Hfree, free, trace = box.QPsolve()
    # print trace