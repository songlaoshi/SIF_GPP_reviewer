function [num_nan]=get_num_of_nan(data)
%%
%计算数列中nan的个数
%%
len=size(data,1);
plen=len/3; % 15个数据，分成3部分，每部分5个
mor=data(1:plen); % 第一部分
noon=data(plen+1:plen*2); %第二部分
aft=data(plen*2+1:len); % 第三部分
num_nan.mor=sum(isnan(mor)); % 第一部分的空值个数
num_nan.noon=sum(isnan(noon)); %第二部分的空值个数
num_nan.aft=sum(isnan(aft)); %第三部分的空值个数
num_nan.all=sum(isnan(data)); %全部空值个数