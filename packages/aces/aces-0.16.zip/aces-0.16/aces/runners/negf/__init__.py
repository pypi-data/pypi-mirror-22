#encoding:utf8
from aces.tools import *
import aces.config as config
from ase import io
from ase.io.vasp import write_vasp
from aces.runners import Runner
from aces.graph import plot,series
import numpy as np
from aces.runners.minimize import minimize as minimize_input
from aces.runners.phonopy import runner as PRunner
from importlib import import_module as im
import time
from numpy.linalg import norm
from aces.f import readfc2
from aces.io.phonopy.fc import nomalizeFC
hbar=6.6260755e-34/3.14159/2.0
kb=1.3806488e-23
def BE(w,T):
	w=np.array(w)
	t= hbar*w/kb/T
	#return np.exp(-t)
	return 1.0/(np.exp(t)-1.0000001)
class runner(Runner):
	def creatmini(self,m):
		print 'creatmini'
		m.home=pwd()
		assert m.home!=''
		mkdir('minimize')
		cd('minimize')
		minimize_input(m)
		write(time.strftime('%Y-%m-%d %H:%M:%S'),'done')
		cd('..')
		return m.dump2POSCAR(m.home+'/minimize/range')
	def test(self):
		dm=.1
		omega=np.arange(dm,60,dm)#THz
		factor=1e12**2*1e-20*1e-3/1.6e-19/6.23e23
		energies=(omega*2.0*np.pi)**2*factor
		#energies=np.arange(0,10,.01)
		h = -np.array((-2, 1,0, 1, -2,1,0,1,-2)).reshape((3,3))
		h1 = -np.array((-2, 1, 1, -2)).reshape((2,2))
		#x=1.0/np.sqrt(2)
		#h1=h=-np.array((-2,x,0,0,x,-1,x,0,0,x,-2,x,0,0,x,-1)).reshape((4,4))
		#energies = np.arange(-3, 3, 0.1)
		calc = TransportCalculator(h=h, h1=h1, energies=energies,dos=True)
		T = calc.get_transmission()
		#print T
		dos=calc.get_dos()*omega
		plot([omega,'Frequency (THz)'],[T,'Transmission'],'test_green_transmission.png')
		plot([omega,'Frequency (THz)'],[dos,'Phonon Density of State'],'test_green_dos.png')
	"""
	def collect(self):		
		leadm=self.preLead()
		fclead=self.fc('lead')
		fccenter=self.fc('center')
		#write(np.around(fc[:,:,0,0],3),'orig_forces')
		n=leadm.hatom
		fccenter[:n,-n:]=0
		fccenter[-n:,:n]=0
		#write(np.around(fccenter[:,:,0,0],3),'fccenter')
		fclead=fclead[:2*n][:2*n]
		fccenter=self.reshape(fccenter)
		fclead=self.reshape(fclead)	
		return fccenter,fclead
	"""
	def collect(self):
		fcleft=self.fc('leftlead')
		write(np.around(fcleft[:,:,0,0],3),'fcleft')
		fcleft=self.reshape(fcleft)
		fcright=self.fc('rightlead')	
		write(np.around(fcright[:,:,0,0],3),'fcright')
		fcright=self.reshape(fcright)	
		fccenter=self.fc('center')
		write(np.around(fccenter[:,:,0,0],3),'fccenter')
		fccenter=self.reshape(fccenter)
		return fccenter,fcleft,fcright
	def gettrans(self):
		print("Reading in force constants...")
		#if not exists("fcbin.npz"):
		fccenter,fcleft,fcright=self.collect()
		np.savez("fcbin.npz",fccenter=fccenter,fcleft=fcleft,fcright=fcright)
		print("Caching force constans")
		import os
		m=self.m
		os.system(config.mpirun+" "+str(m.cores)+" ae trans_cal >log.out")
	def reduce(self):
		files=ls("tmp/result.txt*")
		omega=[]
		trans=[]
		dos=[]
		for file in files:
			result=np.loadtxt(file,skiprows=1)
			omega.append(result[:,0])
			trans.append(result[:,1])
			dos.append(result[:,2])

		omega=np.array(omega).flatten().T
		f=omega.argsort()
		omega=omega[f]
		trans=np.array(trans).flatten().T[f]
		dos=np.array(dos).flatten().T[f]
		to_txt(['omega','trans','dos'],np.c_[omega,trans,dos],'result.txt')
	def generate(self):
		self.m.xp=1
		#leadm=self.preLead()
		#self.phonopy('lead',leadm)
		centerm=self.preCenter()
		self.phonopy('center',centerm)
		self.getlead()
		self.gettrans()
		self.post()
	def post(self):
		#1eV = 8049 cm^(-1) => 1000emV=8049 cm-1 => cm-1/meV=1000/8049
		#1cm^(-1) = 3 * 10^(10) hz =>Hz*cm=1/3e10
		#a cm^-1=b THz =>a=b *1e12 Hz*cm
		#a meV = b cm^-1 => a = b cm-1/meV
		#omcm=omega*521.471？
		self.reduce()
		result=np.loadtxt("result.txt",skiprows=1)
		omega=result[:,0]
		trans =result[:,1]
		dos   =result[:,2]
		omcm=omega*1e12*1/3e10
		omme=omcm *1e12*6.6260755e-34/1.6e-19*1000
		w=omega*1e12*2.0*np.pi
		T=self.m.T
		centerm=self.preCenter()
		V=np.linalg.det(centerm.atoms.cell)
		c=hbar*w*(BE(w,T+0.005)-BE(w,T-0.005))*100.0/V*1e30
		j=c*trans/2.0/np.pi
		dm=omega[1]-omega[0]
		kappa=j.cumsum()*dm
		to_txt(['Frequency (THz)',
				'Frequency (cm^-1)',
				'Frequency (meV)',
				'Phonon Transmission',
				'Phonon Density of State',
				'Mode Capacity (J/m^3/K)',
				'Mode Thermal Conductance (W/m^2/K)',
				'Accumulate Thermal Conductance (W/m^2/K)'
			],
		np.c_[omega,omcm,omme,trans,dos,c,j,kappa],'transmission.txt')
		
		f=np.loadtxt('transmission.txt',skiprows=1)
		plot([f[:,0],'Frequency (THz)'],[f[:,4],'Phonon Density of State'],'green_dos.png')
		plot([f[:,0],'Frequency (THz)'],[f[:,3],'Phonon Transmission'],'green_transmission.png')
		plot([f[:,0],'Frequency (THz)'],[f[:,6],'Mode Thermal Conductance (W/m^2/K)'],'green_mode_conductance.png')
	def reshape(self,fc):
		n,m=fc.shape[:2]
		fc=np.einsum('ikjl',fc).reshape([n*3,m*3])
		return fc
	def testfc(self):
		self.fc('center')
	def fc(self,dir):
		fc=readfc2(dir+'/FORCE_CONSTANTS')
		satoms=io.read(dir+'/SPOSCAR')

		# divide m_i*mj
		
		fc=nomalizeFC(fc,satoms)		
		if not dir=='center':
			atoms=io.read(dir+'/POSCAR')

			fc=self.rearangefc(fc,satoms,atoms)
		else:
			left=io.read(dir+'/POSCAR_left')
			right=io.read(dir+'/POSCAR_right')
			# why not record the order when generating POSCAR_left ? because atoms order may be changed after write to POSCAR
			fc=self.rearangefc_center(fc,satoms,left,right)

		return fc
	def phonopy(self,dir,mm):
		#if exists(dir+'/FORCE_CONSTANTS'):
		#	return
		mkcd(dir)	
		self.creatmini(mm)
		PRunner(mm).generate()
		cd('..')
		
	def preCenter(self):
		m=self.m
		import device.device as s
		leadm=self.preLead()
		u=s.Device(m,leadm,leadm)
		u.cores=m.cores
		u.__dict__=dict(m.__dict__,**u.__dict__)
		return u
	def findunit(self,atoms,rightx,la,end="right",err=0.4):
		"""[find atoms within the period]
		
		[filter the atoms with x > rightx-la (if end=='right') and use la as lattice constant to build a new unitcell]
		
		Arguments:
			atoms {[Atoms]} -- [The center region atoms of NEGF, with scatter part and left and right lead part of 2 layers]
			rightx {[Nubmer]} -- [the x position of right most atom]
			la {[Number]} -- [the lattice constant of result unitcell]
		
		Keyword Arguments:
			end {str} -- [which lead do you want ,can be 'left' and 'right'] (default: {"right"})
			err {number} -- [the tolerence to find an atom ] (default: {0.3})
		
		Returns:
			[Atoms] -- [The result unitcell]
		"""
		
		from ase import Atoms
		if end=="right":
			fil=atoms.positions[:,0]>rightx-la-err
			offset=[la,0,0]
		else:
			fil=atoms.positions[:,0]<rightx+la+err
			offset=[-la,0,0]
		patoms=atoms[fil]

		# exclude the atoms that could be get though move one righer atom
		invalids=[]
		for p in patoms:
			for i,q in enumerate(patoms):
				if norm(q.position+offset-p.position)<err and q.symbol==p.symbol:
					invalids.append(i)
		qatoms=Atoms()
		for i,q in enumerate(patoms):
			if i in invalids:
				continue
			qatoms.append(q)

		# check qatoms is a unitcell
		isunit=[False]*len(qatoms)
		for i,p in enumerate(qatoms):
			for q in atoms:
				if norm(p.position-offset-q.position)<err and q.symbol==p.symbol:
					isunit[i]=True
					break
		print "is maching:",isunit
		# the unitcell must exist
		#assert reduce(lambda a,b:a*b,isunit)
		return qatoms	

	def getlead(self):
		cd('center')
		left=self.findlead('left')
		right=self.findlead('right')
		cd('..')
		from aces.io.vasp import writevasp
		mkdir('leftlead')
		mkdir('rightlead')
		writevasp(left,'leftlead/POSCAR')
		writevasp(right,'rightlead/POSCAR')
		cd('leftlead')
		self.runlead()
		cd('..')
		cd('rightlead')
		self.runlead()
		cd('..')

	def findlead(self,end="left",err=0.3):
		"""[from center POSCAR find periodic lead POSCAR]
		
		[the center POSCAR is expected to consist of scatter region and left lead region of 2 layers and 
		right lead region of 2 layers. So we can find the lead POSCAR from the two ends with this algorithm.]
		
		Keyword Arguments:
			end {str} -- [which lead do you want ,can be 'left' and 'right'] (default: {"left"})
			err {number} -- [the tolerence to find an atom ] (default: {0.4})
		
		Raises:
			Exception -- [end is not set correctly]
		"""
		
		from ase import io ,Atoms
		atoms=io.read('POSCAR')
		# find the most right atom index
		if end=="right":
			last=-1
			next_last=-2
		elif end=="left":
			last=0
			next_last=1
		else:
			raise Exception("Unkown value of `end`")
		right_idx=atoms.positions[:,0].argsort()[last]
		ratom=atoms[right_idx]
		print "%s end atom position:"%end,ratom.position
		# the atoms that has similar y,z to ratom , in our situatoin there is at least two such atoms.
		fil=norm(atoms.positions[:,1:]-ratom.position[1:],axis=1)<err
		# Don't forget the symbol must be the same.
		# must convert to array
		fil1=np.array(atoms.get_chemical_symbols())==ratom.symbol
		fil=fil*fil1
		atoms_inline=atoms[fil]
		assert len(atoms_inline)>=2
		right_idx1=atoms_inline.positions[:,0].argsort()[next_last]
		# waring this index is of atoms_inline but not of atoms
		# catom is what we search
		catom=atoms_inline[right_idx1]
		print "next %s end similar atom position:"%end,catom.position
		# the possible lattice constant of x direction 
		la=np.abs(ratom.position[0]-catom.position[0])
		rightx=ratom.position[0]
		unit=self.findunit(atoms,rightx,la,end,err)
		if end=="right":
			unit.translate([-(rightx-la),0,0])
		else:
			unit.translate([-(rightx),0,0])
		unit.cell=atoms.cell
		unit.cell[0,0]=la
		#unit.center(axis=0)
		from aces.io.vasp import writevasp
		writevasp(unit,'POSCAR_%s'%end)
		return unit
	def runlead(self):
		"""generate lead force constants
		
		TRICK!!
		> If hc1/hc2 are None, they are assumed to be identical to the coupling matrix elements between neareste neighbor principal layers in lead1/lead2.

		3 is important for the NEGF calculation ,if use 2, the regurlar fc and periodic fc is undistinguable,
		1 -1 
		-1 1

		and the transimission is curve
		for example ,
		the fclead should be when lead layer=1,and two layer interaction is 
		2 -1
		-1 2
		and we can get from 3 layer supercell by  fc[:2n,:2n] , this process will complete in rearangefc
		2 -1 -1 
		-1 2 -1 
		-1 2 2
		
		"""
		m=self.m
		s=im('aces.materials.graphene')
		mm=s.structure(dict(latx=1,laty=1,latz=1,xp=1,yp=0,zp=0))
		mm.atoms=io.read("POSCAR")

		mm.supercell=[3,1,1]
		mm.phofc=True
		mm.__dict__=dict(m.__dict__,**mm.__dict__)
		PRunner(mm).run()
	def preLead(self):
		m=self.m
		s=im('aces.materials.%s'%m.leads)
		lat=m.leadlat
		mm=s.structure(dict(latx=lat[0],laty=lat[1],latz=lat[2],xp=1,yp=1,zp=1))
		mm.dimension=m.dimension
		import device.lead as s
		u=s.Lead(mm)
		#u.cores=m.cores
		u.__dict__=dict(m.__dict__,**u.__dict__)
		return u
	def rearangefc_center(self,fc,satoms,left,right):
		right_idx=satoms.positions[:,0].argsort()[-1]
		x_right=satoms[right_idx].position[0]
		left_idx=satoms.positions[:,0].argsort()[0]
		x_left=satoms[left_idx].position[0]
		# find the index of left part in satoms
		atoms=left.copy()
		# remove the offset
		atoms.translate([x_left,0,0])
		lidx=self.match_idx(atoms,satoms)
		lidx=list(lidx)
		# find the index of right part in satoms
		atoms=right.copy()

		atoms.translate([x_right-right.cell[0,0],0,0])

		ridx=self.match_idx(atoms,satoms)
		ridx=list(ridx)
		# find the center index
		cidx=[]
		for i in range(len(satoms)):
			if i in lidx:continue
			if i in ridx:continue
			cidx.append(i)
		order= lidx+cidx+ridx
		print order
		newfc=fc[order][:,order]
		n1=len(lidx)
		n2=len(ridx)
		# eliminate periodic effect ,which is very important
		newfc[:n1][:,-n2:]=0
		newfc[-n2:][:,:n1]=0
		return newfc


	def match_idx(self,atoms,satoms,err=0.4):
		"""find the indexes of atoms in satoms with the same position
		
		[description]
		
		Arguments:
			atoms {[type]} -- [description]
			satoms {[type]} -- [description]
			err {Number} -- tolerance for position compare
		"""
		natom=len(atoms)
		idx=-np.ones(natom)
		for i,p in enumerate(atoms):
			for j,q in enumerate(satoms):
				if norm(q.position-p.position)<err  and q.symbol==p.symbol:
					idx[i]=j
				if norm(q.position+satoms.cell[0]-p.position)<err  and q.symbol==p.symbol:
					idx[i]=j
					break
		# there must be a match atom
		assert (idx>=0).all()

		return idx
	def rearangefc(self,fc,satoms,atoms):
		"""[ reorder fc by satoms-> atoms +atoms ]
		
		the order of atoms in SPOSCAR is not [atoms in left+ atoms in right] but may be random 
		for example ,the atoms in POSCAR is C4N4 then the order in SPOSCAR is C8N8 however we need C4N4+C4N4
		
		if we get the order = [0,4,1,5,2,6,3,7] ,which means newfc[1]=fc[4]
		then we have newfc[i]=fc[order[i]]=fc[order][i] => newfc=fc[order]
		more acurately because fc.dimension=2 we must have newfc=fc[order][:,order]
		
		Arguments:
			fc {[type]} -- [description]
			stoms {[type]} -- [description]
			atoms {[type]} -- [description]
		
		Returns:
			[type] -- [description]
		"""
		
		#from aces.f import mapatoms,writefc2
		#pos,order=mapatoms(atoms,old)
		#old.write('old.xyz')
		#atoms[order].write('new.xyz')
		
		# find the index of left part in satoms
		lidx=self.match_idx(atoms,satoms)
		lidx=list(lidx)

		# find the index of right part in satoms
		ratoms=atoms.copy()
		ratoms.translate(satoms.cell[0]-atoms.cell[0])
		ridx=self.match_idx(ratoms,satoms)
		ridx=list(ridx)
		# concat them 
		cidx=[]
		for i in range(len(satoms)):
			if i in lidx:continue
			if i in ridx:continue
			cidx.append(i)
		order= lidx+cidx+ridx
		print order
		print satoms.positions[order]
		newfc=fc[order][:,order]
		return newfc[:2*len(atoms),:2*len(atoms)]
		## generated from aces.io.vasp.writevasp to record original order of atoms 
		#order=np.loadtxt(dir+'/POSCARswap').astype(np.int)
		##writefc2(fc[order][:,order],'fc')
		#return fc[order][:,order]
