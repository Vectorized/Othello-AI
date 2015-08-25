import array, os

diag4  = [None] * 13
diag5  = [None] * 13
diag6  = [None] * 13
diag7  = [None] * 13
diag8  = [None] * 13
lc1    = [None] * 13
lc2    = [None] * 13
lc3    = [None] * 13
lc4    = [None] * 13
corn   = [None] * 13
parity = [None] * 13

cwd = os.path.curdir
for s in xrange(13):
	diag4[s]  = array.array('i'); diag4[s] .fromfile(open(os.path.join(cwd, 'patterns', 'diag4_%d'%s), 'rb'),  81);
	diag5[s]  = array.array('i'); diag5[s] .fromfile(open(os.path.join(cwd, 'patterns', 'diag5_%d'%s), 'rb'),  243);
	diag6[s]  = array.array('i'); diag6[s] .fromfile(open(os.path.join(cwd, 'patterns', 'diag6_%d'%s), 'rb'),  729);
	diag7[s]  = array.array('i'); diag7[s] .fromfile(open(os.path.join(cwd, 'patterns', 'diag7_%d'%s), 'rb'),  2187);
	diag8[s]  = array.array('i'); diag8[s] .fromfile(open(os.path.join(cwd, 'patterns', 'diag8_%d'%s), 'rb'),  6561);
	lc1[s]    = array.array('i'); lc1[s]   .fromfile(open(os.path.join(cwd, 'patterns', 'lc1_%d'  %s), 'rb'),  6561);
	lc2[s]    = array.array('i'); lc2[s]   .fromfile(open(os.path.join(cwd, 'patterns', 'lc2_%d'  %s), 'rb'),  6561);
	lc3[s]    = array.array('i'); lc3[s]   .fromfile(open(os.path.join(cwd, 'patterns', 'lc3_%d'  %s), 'rb'),  6561);
	lc4[s]    = array.array('i'); lc4[s]   .fromfile(open(os.path.join(cwd, 'patterns', 'lc4_%d'  %s), 'rb'),  6561);
	corn[s]   = array.array('i'); corn[s]  .fromfile(open(os.path.join(cwd, 'patterns', 'corn_%d' %s), 'rb'),  6561);
	parity[s] = array.array('i'); parity[s].fromfile(open(os.path.join(cwd, 'patterns', 'parity_%d'%s), 'rb'), 2);
