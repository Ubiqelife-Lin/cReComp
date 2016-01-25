#!/usr/bin/python
# -*- coding: utf-8 -*-
import common
class Fifo_32(object):
	"""docstring for Fifo_32"""
	def __init__(self):
		self.reg2fifo_stack_32_r = []
		self.bit_witdh_32_r = []
		self.reg2fifo_stack_32_s = []
		self.bit_witdh_32_s = []

	def gen_reg(self,flag,fo):
		fo.write("\n\n")
		fo.write("//for 32bbit FIFO\n")
		i = 0
		j = 0
		k = 0
		cur_r = 0
		cur_s = 0
		while i < len(flag.alw32_stack):
			reg2fifo = flag.alw32_stack[i].split(",")

			if len(reg2fifo) > 2 and len(reg2fifo) < 5 and reg2fifo[1].isdigit() and (reg2fifo[0]=="r" or reg2fifo[0]=="w") and reg2fifo[2]!="":
				pass
			else:
				print "error ports declaration"
				print "not generated"
				print reg2fifo
				common.remove_file(fo,flag.module_name)
				quit()
			if cur_r > 32:
				print "error! Upper limit of 32bit FIFO was exceeded"
				cur_r = cur_r - int(reg2fifo[1])
				break;
			elif cur_s > 32:
				print "error! Upper limit of 32bit FIFO was exceeded"
				cur_s = cur_s - int(reg2fifo[1])
				break;
			elif reg2fifo[0] == "r":
				if len(reg2fifo) > 3:
					n = 0
					if "x" in reg2fifo[3]:
						pass
					else:
						print "syntax error"
						print reg2fifo
						common.remove_file(fo,flag.module_name)
						quit()
					while n < int(reg2fifo[3].translate(None,"x")):
						self.bit_witdh_32_r.append(reg2fifo[1])
						self.reg2fifo_stack_32_r.append("%s_%s"%(reg2fifo[2],n))
						fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_32_r[j+n])-1,self.reg2fifo_stack_32_r[j+n]))
						cur_r = cur_r + int(reg2fifo[1])
						n = n + 1
					j = j + n
				else:
					self.bit_witdh_32_r.append(reg2fifo[1])
					self.reg2fifo_stack_32_r.append(reg2fifo[2])
					fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_32_r[j])-1,self.reg2fifo_stack_32_r[j]))
					cur_r = cur_r + int(reg2fifo[1])
					j = j + 1

			elif reg2fifo[0] == "w":
				if len(reg2fifo) > 3:
					n = 0
					if "x" in reg2fifo[3]:
						pass
					else:
						print "syntax error"
						print reg2fifo
						common.remove_file(fo,flag.module_name)
						quit()
					while n < int(reg2fifo[3].translate(None,"x")):
						self.bit_witdh_32_s.append(reg2fifo[1])
						self.reg2fifo_stack_32_s.append("%s_%s"%(reg2fifo[2],n))
						fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_32_s[k+n])-1,self.reg2fifo_stack_32_s[k+n]))
						cur_s = cur_s + int(reg2fifo[1])
						n = n + 1
					k = k + n
				else:
					self.bit_witdh_32_s.append(reg2fifo[1])
					self.reg2fifo_stack_32_s.append(reg2fifo[2])
					fo.write("reg [%s:0] %s;\n"%(int(self.bit_witdh_32_s[k])-1,self.reg2fifo_stack_32_s[k]))
					cur_s = cur_s + int(reg2fifo[1])
					k = k + 1

			i = i + 1

	def gen_alw(self,flag,fo):
		i = 0
		bitmin = 0
		bitmax = 0
		ans_hs_m =""
		# if flag.module_type == "hs_mst":
		# 	ans_hs_m = True
		# elif flag.module_type == "normal":
		# 	ans_hs_m = False

		fi = open("lib/lib_alw32")
		while True:
			l = fi.readline().rstrip()
			if l == "/*user defined init*/":
				fo.write(l+"\n")
				break
			fo.write(l+"\n")
		if len(self.reg2fifo_stack_32_r) > 0:
			while i < len(self.reg2fifo_stack_32_r):
				fo.write("\t\t%s <= 0;\n"%self.reg2fifo_stack_32_r[i])
				i = i + 1
		while True:
			l = fi.readline().rstrip()
			if l == "/*user defined rcv*/":
				fo.write(l+"\n")
				break
			fo.write(l+"\n")
		i = 0
		if len(self.reg2fifo_stack_32_r) > 0:
			while i < len(self.reg2fifo_stack_32_r):
				bitmax = bitmin + int(self.bit_witdh_32_r[i]) - 1;
				fo.write("\t\t%s <= rcv_data_32[%s:%s];\n"%(self.reg2fifo_stack_32_r[i],bitmax,bitmin))
				i = i + 1
				bitmin = bitmax + 1
		while True:
			l = fi.readline().rstrip()
			if l == "/*user assign*/":
				fo.write(l+"\n")
				break
			fo.write(l+"\n")
		i = 0
		bitmin = 0
		if len(self.reg2fifo_stack_32_s) > 0:
			while i < len(self.reg2fifo_stack_32_s):
				bitmax = bitmin + int(self.bit_witdh_32_s[i]) - 1
				fo.write("assign snd_data_32[%s:%s] = %s;\n"%(bitmax,bitmin,self.reg2fifo_stack_32_s[i]))
				i = i + 1
				bitmin = bitmax + 1

		# if ans_hs_m and len(flag.sub_module_name)>0:
		# 	i = 0
		# 	while i < len(flag.sub_module_name):
		# 		fi = open("lib/hs_mst_alw32")
		# 		while l in fi.readline():
		# 			l = l.translate("req_%s"%flag.sub_module_name[i],"/*req*/")
		# 			l = l.translate("busy_%s"%flag.sub_module_name[i],"/*busy*/")
		# 			l = l.translate("finish_%s"%flag.sub_module_name[i],"/*finish*/")
		# 			fo.write(l)
		# 		i = i + 1
		while l in fi.readline():
			fo.write(l)
