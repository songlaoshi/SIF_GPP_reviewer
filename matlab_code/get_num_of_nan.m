function [num_nan]=get_num_of_nan(data)
%%
%����������nan�ĸ���
%%
len=size(data,1);
plen=len/3; % 15�����ݣ��ֳ�3���֣�ÿ����5��
mor=data(1:plen); % ��һ����
noon=data(plen+1:plen*2); %�ڶ�����
aft=data(plen*2+1:len); % ��������
num_nan.mor=sum(isnan(mor)); % ��һ���ֵĿ�ֵ����
num_nan.noon=sum(isnan(noon)); %�ڶ����ֵĿ�ֵ����
num_nan.aft=sum(isnan(aft)); %�������ֵĿ�ֵ����
num_nan.all=sum(isnan(data)); %ȫ����ֵ����