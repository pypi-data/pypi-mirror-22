
def print_lol(the_list,level=0):
	"""
	�������ȡһ��λ�ò�������Ϊ��the_list����
	 ��������κ�python�б�Ҳ�����ǰ���Ƕ���б���б�
	��ָ�����б��е�ÿ��������ᣨ�ݹ�أ��������Ļ�ϣ����������վһ�С�
	"""
	for e_item in the_list:
		if isinstance(e_item,list):
			print_lol(e_item,level+1)
		else:
			for tab_stop in range(level):
				    print('--------------------')
			print(e_item)
