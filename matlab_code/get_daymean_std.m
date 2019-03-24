path='D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data';
[data,text]=xlsread([path '\SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx']);
addpath('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab_code');

gpp=data(:,3);
sif=data(:,11);

Daymean=[];Daystd=[];
count1=1;
count2=1;
for i=1:15:size(data,1)
    gpp_numnan=get_num_of_nan(gpp(i:i+14));
    sif_numnan=get_num_of_nan(sif(i:i+14));
    
    daymean=nanmean(data(i:i+14,:),1);
    daystd=nanstd(data(i:i+14,:),1);
    
    if gpp_numnan.mor==5 || gpp_numnan.noon==5 || gpp_numnan.aft==5 || gpp_numnan.all>=8
        daymean(1,[3,18])=nan;
        daystd(1,[3,18])=nan;
        count1=count1+1;
    end
    if sif_numnan.mor==5 || sif_numnan.noon==5 || sif_numnan.aft==5 || sif_numnan.all>=8
        daymean(1,[9,10,11,15,16,17])=nan;
        daystd(1,[9,10,11,15,16,17])=nan;
        count2=count2+1;
    end

    Daymean=[Daymean;daymean];
    Daystd=[Daystd;daystd];
end
xlswrite([path '\SIF_GPP_VI_ref_daymean_sq2017corn.xlsx'],text,1,'A1');
xlswrite([path '\SIF_GPP_VI_ref_daymean_sq2017corn.xlsx'],Daymean,1,'A2');
xlswrite([path '\SIF_GPP_VI_ref_daymean_sq2017corn.xlsx'],text,2,'A1');
xlswrite([path '\SIF_GPP_VI_ref_daymean_sq2017corn.xlsx'],Daystd,2,'A2');

% xlswrite([path '\SIF_GPP_VI_ref_daymean_sq2017corn_nocontrol.xlsx'],text,1,'A1');
% xlswrite([path '\SIF_GPP_VI_ref_daymean_sq2017corn_nocontrol.xlsx'],Daymean,1,'A2');
% xlswrite([path '\SIF_GPP_VI_ref_daymean_sq2017corn_nocontrol.xlsx'],text,2,'A1');
% xlswrite([path '\SIF_GPP_VI_ref_daymean_sq2017corn_nocontrol.xlsx'],Daystd,2,'A2');