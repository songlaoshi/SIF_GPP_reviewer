clear;
clc;
addpath('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab code');
path='D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data\';
savepath='D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data\sunny_cloudy_data\';
Temp3=xlsread([path 'SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx']);
idx=Temp3(:,1)>=205 & Temp3(:,1)<255;
GPP=Temp3(idx,:);
sunnySIF=[];cloudySIF=[];
sunnyGPP=[];cloudyGPP=[];
sunnyVPD=[];cloudyVPD=[];
sunnyTa=[];cloudyTa=[];
sunnyPAR=[];cloudyPAR=[];
sunnyAPAR=[];cloudyAPAR=[];

ci_threshold=0.75;
ci_threshold1=0.5;
% ci_threshold=10;
% 10/15
for i=1:15:size(GPP,1)
    daymeanCI=nanmean(GPP(i:i+14,14));
%     ci=GPP(i:i+14,14);
%     daymeanCI=sum(ci>0.55);
    
    sif=GPP(i:i+14,11);
    gpp=GPP(i:i+14,3);
    vpd=GPP(i:i+14,4);
    ta=GPP(i:i+14,5);
    par=GPP(i:i+14,7);
    apar=GPP(i:i+14,19);
    
    gpp_numnan=get_num_of_nan(gpp);
    sif_numnan=get_num_of_nan(sif);
    
    if daymeanCI>ci_threshold && gpp_numnan.mor<=2 && gpp_numnan.noon<=2 && gpp_numnan.aft<=2 && gpp_numnan.all<=7
        sunnyGPP=[sunnyGPP gpp];
        sunnyVPD=[sunnyVPD vpd];
        sunnyTa=[sunnyTa ta];
        sunnyPAR=[sunnyPAR par];
        sunnyAPAR=[sunnyAPAR apar];
    end
    if daymeanCI<=ci_threshold1 && gpp_numnan.mor<=2 && gpp_numnan.noon<=2 && gpp_numnan.aft<=2 && gpp_numnan.all<=7
        cloudyGPP=[cloudyGPP gpp];
        cloudyVPD=[cloudyVPD vpd];
        cloudyTa=[cloudyTa ta];
        cloudyPAR=[cloudyPAR par];
        cloudyAPAR=[cloudyAPAR apar];
    end
    if daymeanCI>ci_threshold && sif_numnan.mor<=2 && sif_numnan.noon<=2 && sif_numnan.aft<=2 && sif_numnan.all<=7
        sunnySIF=[sunnySIF sif];
    end
    if daymeanCI<=ci_threshold1 && gpp_numnan.mor<=2 && sif_numnan.noon<=2 && sif_numnan.aft<=2 && sif_numnan.all<=7
        cloudySIF=[cloudySIF sif];
    end
end
% xlswrite([savepath 'SIF_PAR_sunny_halfhour_all.xlsx'],sunnySIF,'sunnySIF','A1');
% xlswrite([savepath 'SIF_PAR_sunny_halfhour_all.xlsx'],sunnyPAR,'sunnyPAR','A1');
% xlswrite([savepath 'SIF_PAR_sunny_halfhour_all.xlsx'],sunnyGPP,'sunnyGPP','A1');
% xlswrite([savepath 'SIF_PAR_cloudy_halfhour_all.xlsx'],cloudySIF,'cloudySIF','A1');
% xlswrite([savepath 'SIF_PAR_cloudy_halfhour_all.xlsx'],cloudyPAR,'cloudyPAR','A1');
% xlswrite([savepath 'SIF_PAR_cloudy_halfhour_all.xlsx'],cloudyGPP,'cloudyGPP','A1');

sunnymeanSIF=nanmean(sunnySIF,2);
sunnymeanGPP=nanmean(sunnyGPP,2);
sunnymeanVPD=nanmean(sunnyVPD,2);
sunnymeanTa=nanmean(sunnyTa,2);
sunnymeanPAR=nanmean(sunnyPAR,2);
sunnymeanAPAR=nanmean(sunnyAPAR,2);
cloudymeanSIF=nanmean(cloudySIF,2);
cloudymeanGPP=nanmean(cloudyGPP,2);
cloudymeanVPD=nanmean(cloudyVPD,2);
cloudymeanTa=nanmean(cloudyTa,2);
cloudymeanPAR=nanmean(cloudyPAR,2);
    cloudymeanAPAR=nanmean(cloudyAPAR,2);
temp=[sunnymeanSIF sunnymeanGPP sunnymeanVPD sunnymeanTa sunnymeanPAR sunnymeanAPAR ...
    cloudymeanSIF cloudymeanGPP cloudymeanVPD cloudymeanTa cloudymeanPAR cloudymeanAPAR];
time=9:0.5:16;
title={'time','sunnysif','sunnygpp','sunnyvpd','sunnyta','sunnypar','sunnyapar', ...
    'cloudysif','cloudygpp','cloudyvpd','cloudyta','cloudypar','cloudyapar'};
xlswrite([savepath 'SIF_GPP_VPD_Ta_PAR_APAR_morning_afternoon_diurnal_average.xlsx'],title,1,'A1');
xlswrite([savepath 'SIF_GPP_VPD_Ta_PAR_APAR_morning_afternoon_diurnal_average.xlsx'],[time' temp],1,'A2');
% %% plot sif par hystresis
% morsif=temp(1:7,1);
% morpar=temp(1:7,5);
% aftersif=temp(8:end,1);
% afterpar=temp(8:end,5);
% figure
% subplot(211)
% plot(morpar,morsif,'bo-');
% hold on
% plot(afterpar,aftersif,'ro-');
% subplot(212)
% plot(morpar,temp(1:7,2),'bo-');
% hold on
% plot(afterpar,temp(8:end,2),'ro-');
%%
% %%
% sunnySIF=[];cloudySIF=[];
% sunnyGPP=[];cloudyGPP=[];
% sunnyVPD=[];cloudyVPD=[];
% sunnyTa=[];cloudyTa=[];
% sunnyPAR=[];cloudyPAR=[];
% sunnyAPAR=[];cloudyAPAR=[];
% for i=1:20:size(GPP,1)
%     daymeanCI=nanmean(GPP(i:i+19,32));
%     
%     sifm=GPP(i:i+9,13);sifa=GPP(i+10:i+19,13);
%     gppm=GPP(i:i+9,3);gppa=GPP(i+10:i+19,3);
%     vpdm=GPP(i:i+9,4);vpda=GPP(i+10:i+19,4);
%     tam=GPP(i:i+9,5);taa=GPP(i+10:i+19,5);
%     parm=GPP(i:i+9,7);para=GPP(i+10:i+19,7);
%     aparm=GPP(i:i+9,8);apara=GPP(i+10:i+19,8);
%     
%     if daymeanCI>0.5
%         sunnySIF=[sunnySIF ;sifm sifa];
%         sunnyGPP=[sunnyGPP ;gppm gppa];
%         sunnyVPD=[sunnyVPD ;vpdm vpda];
%         sunnyTa=[sunnyTa ;tam taa];
%         sunnyPAR=[sunnyPAR ;parm para];
%         sunnyAPAR=[sunnyAPAR ;aparm apara];
%     else
%         cloudySIF=[cloudySIF ;sifm sifa];
%         cloudyGPP=[cloudyGPP ;gppm gppa];
%         cloudyVPD=[cloudyVPD ;vpdm vpda];
%         cloudyTa=[cloudyTa ;tam taa];
%         cloudyPAR=[cloudyPAR ;parm para];
%         cloudyAPAR=[cloudyAPAR ;aparm apara];
%     end
% end
% temp=[sunnySIF sunnyGPP sunnyVPD sunnyTa sunnyPAR sunnyAPAR];
% title={'sifm','sifa','gppm','gppa','vpdm','vpda','tam','taa','parm','para','aparm','apara'};
% xlswrite([path 'SIF_GPP_VPD_Ta_PAR_APAR_morning_afternoon_sunny.xlsx'],title,1,'A1');
% xlswrite([path 'SIF_GPP_VPD_Ta_PAR_APAR_morning_afternoon_sunny.xlsx'],temp,1,'A2');
% temp=[cloudySIF cloudyGPP cloudyVPD cloudyTa cloudyPAR cloudyAPAR];
% xlswrite([path 'SIF_GPP_VPD_Ta_PAR_APAR_morning_afternoon_cloudy.xlsx'],title,1,'A1');
% xlswrite([path 'SIF_GPP_VPD_Ta_PAR_APAR_morning_afternoon_cloudy.xlsx'],temp,1,'A2');
%% get growth stage data
Temp3=xlsread([path 'SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx']);
a2 = 205;
a3 = 255;
idx1=Temp3(:,1)<205;
idx2=Temp3(:,1)>=205 & Temp3(:,1)<255;
idx3=Temp3(:,1)>=255;
idx4=ones(size(Temp3(:,1),1),1)==1;

ci_threshold=0.75;

for m=1:4
    idx=eval(['idx' num2str(m)]);
    GPP=Temp3(idx,:);
    
    sunnySIF=[];cloudySIF=[];
    sunnyPAR=[];cloudyPAR=[];
    sunnyAPAR=[];cloudyAPAR=[];

    for i=1:15:size(GPP,1)
        daymeanCI=nanmean(GPP(i:i+14,14));

        sif=GPP(i:i+14,11);
        gpp=GPP(i:i+14,3);
        vpd=GPP(i:i+14,4);
        ta=GPP(i:i+14,5);
        par=GPP(i:i+14,7);
        apar=GPP(i:i+14,19);
        
        gpp_numnan=get_num_of_nan(gpp);
        sif_numnan=get_num_of_nan(sif);

        if daymeanCI>ci_threshold && gpp_numnan.mor<=2 && gpp_numnan.noon<=2 && gpp_numnan.aft<=2 && gpp_numnan.all<=7
            sunnyPAR=[sunnyPAR par];
            sunnyAPAR=[sunnyAPAR apar];
        end
        if daymeanCI<=ci_threshold && gpp_numnan.mor<=2 && gpp_numnan.noon<=2 && gpp_numnan.aft<=2 && gpp_numnan.all<=7
            cloudyPAR=[cloudyPAR par];
            cloudyAPAR=[cloudyAPAR apar];
        end
        if daymeanCI>ci_threshold && sif_numnan.mor<=2 && sif_numnan.noon<=2 && sif_numnan.aft<=2 && sif_numnan.all<=7
            sunnySIF=[sunnySIF sif];
        end
        if daymeanCI<=ci_threshold && gpp_numnan.mor<=2 && sif_numnan.noon<=2 && sif_numnan.aft<=2 && sif_numnan.all<=7
            cloudySIF=[cloudySIF sif];
        end
    end

    sunnymeanSIF=nanmean(sunnySIF,2);
    sunnymeanPAR=nanmean(sunnyPAR,2);
    sunnymeanAPAR=nanmean(sunnyAPAR,2);
    cloudymeanSIF=nanmean(cloudySIF,2);
    cloudymeanPAR=nanmean(cloudyPAR,2);
    cloudymeanAPAR=nanmean(cloudyAPAR,2);
    temp=[sunnymeanSIF sunnymeanPAR sunnymeanAPAR ...
        cloudymeanSIF cloudymeanPAR cloudymeanAPAR];
    time=9:0.5:16;
    title={'time','sunnysif','sunnypar','sunnyapar', ...
        'cloudysif','cloudypar','cloudyapar'};
    if m==1
        xlswrite([savepath  'SIF_PAR_APAR_morning_afternoon_vege_dailycorrection.xlsx'],title,1,'A1');
        xlswrite([savepath  'SIF_PAR_APAR_morning_afternoon_vege_dailycorrection.xlsx'],[time' temp],1,'A2');
    elseif m==2
        xlswrite([savepath  'SIF_PAR_APAR_morning_afternoon_repro_dailycorrection.xlsx'],title,1,'A1');
        xlswrite([savepath  'SIF_PAR_APAR_morning_afternoon_repro_dailycorrection.xlsx'],[time' temp],1,'A2');
    elseif m==3
        xlswrite([savepath  'SIF_PAR_APAR_morning_afternoon_ripen_dailycorrection.xlsx'],title,1,'A1');
        xlswrite([savepath  'SIF_PAR_APAR_morning_afternoon_ripen_dailycorrection.xlsx'],[time' temp],1,'A2');
    elseif m==4
        xlswrite([savepath  'SIF_PAR_APAR_morning_afternoon_wholeseason_dailycorrection.xlsx'],title,1,'A1');
        xlswrite([savepath  'SIF_PAR_APAR_morning_afternoon_wholeseason_dailycorrection.xlsx'],[time' temp],1,'A2');
    end
end

% %% get everyday's r2 for SIF-GPP, SIFyield-LUE
% r1=[];
% r2=[];
% r3=[];
% r4=[];
% for i=1:20:size(GPP,1)
%     doy=fix(GPP(i,2));
%     sif=GPP(i:i+19,13);
%     gpp=GPP(i:i+19,3);
%     par=GPP(i:i+19,7);
%     apar=GPP(i:i+19,8);
%     sifyield=GPP(i:i+19,37);
%     lue=GPP(i:i+19,41);
%     temp=corrcoef(apar,gpp);
%     apar_gpp=temp(1,2)^2;
%     temp=corrcoef(apar,sif);
%     apar_sif=temp(1,2)^2;
%     temp=corrcoef(sif,gpp);
%     sif_gpp=temp(1,2)^2;
%     temp=corrcoef(sifyield,lue);
%     sifyield_lue=temp(1,2)^2;
%     
%     r1=[r1;doy apar_gpp];
%     r2=[r2;doy apar_sif];
%     r3=[r3;doy sif_gpp];
%     r4=[r4;doy sifyield_lue];
% end
% figure
% subplot(4,1,1)
% bar(r1(:,1),r1(:,2))
% ylabel('APAR-GPP')
% subplot(4,1,2)
% bar(r2(:,1),r2(:,2))
% ylabel('APAR-SIF')
% subplot(4,1,3)
% bar(r3(:,1),r3(:,2))
% ylabel('SIF-GPP')
% subplot(4,1,4)
% bar(r4(:,1),r4(:,2))
% xlabel('DOY')
% ylabel('SIFyield-LUE')
% xlswrite([path '\ALLnew\' 'SIF_PAR_sunny_0.7.xlsx'],[sunnySIF;sunnyPAR],1,'A1');
% xlswrite([path '\ALLnew\' 'SIF_PAR_cloudy_0.7.xlsx'],[cloudySIF;cloudyPAR],1,'A1');