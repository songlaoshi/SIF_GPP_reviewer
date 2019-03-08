path='D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data';
[data,text]=xlsread([path '\SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx']);
addpath('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab code');

sunny=[];cloudy=[];
count1=1;
count2=1;
for i=1:15:size(data,1)
    temp=data(i:i+14,:);
    ci=data(i:i+14,14);
    if sum(ci>0.55)>=8
        sunny=[sunny;temp];
        count1=count1+1;
    else
        cloudy=[cloudy;temp];
        count2=count2+1;
    end
end
xlswrite([path '\SIF_GPP_VI_ref_halfhourmean_sq2017corn_sunny.xlsx'],text,1,'A1');
xlswrite([path '\SIF_GPP_VI_ref_halfhourmean_sq2017corn_sunny.xlsx'],sunny,1,'A2');
xlswrite([path '\SIF_GPP_VI_ref_halfhourmean_sq2017corn_cloudy.xlsx'],text,2,'A1');
xlswrite([path '\SIF_GPP_VI_ref_halfhourmean_sq2017corn_cloudy.xlsx'],cloudy,2,'A2');

