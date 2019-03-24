clear;clc;

irradpath='D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\Radiance\QE\Irradiance';
radpath='D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\Radiance\QE\Radiance';
savepath='D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\SIF_QE_SFM760';
savepath1='D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\SIF_QE_SFM760_atc';
addpath('D:\Data\Xilinhot2017 Code');
addpath('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab_code\atmos_correction');
% 温度，气压数据
Tem_press_all_data=xlsread('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab_code\atmos_correction\Tem_press_all_data.xlsx');

filesirrad=dir([irradpath '\*.xlsx']);
filesrad=dir([radpath '\*.xlsx']);


for i=86:length(filesirrad)
    string_date=filesirrad(i).name(1:8);
    irrad=xlsread([irradpath '\' filesirrad(i).name]);
    rad=xlsread([radpath '\' filesrad(i).name]);    
    % 
    wl=irrad(1,6:end);
%     time=irrad(2:end,5);
    % 
    SIFA=[];
    SIFAatc=[];

    for j=2:size(irrad,1)
        Gnum=irrad(j,1);
        hour=irrad(j,2);mint=irrad(j,3);sec=irrad(j,4);
        time=irrad(j,5);
        Hs_format_time=hour+mint/60+sec/3600;
        Hs=Solar_Altitude(115.5916,34.5199,string_date,Hs_format_time);
        %% 未大气校正sif
        data_irrd=[wl',irrad(j,6:end)'];
        data_rad=[wl',rad(j,6:end)'];

        if min(isnan(data_irrd(:,2)))==1 || min(isnan(data_rad(:,2))==1) || max(data_irrd(:,2))==0
            SIFA=[SIFA;Gnum,hour,mint,sec,time,Hs,nan(1,9)];
            SIFAatc=[SIFAatc;Gnum,hour,mint,sec,time,Hs,nan(1,9)];
            continue;
        else
             fw=0.2;
            %----------------------------sFLD-------------------------------
            [fs_sFLD_A,~,~,~]=sFLD(data_irrd,data_rad,fw);
            %----------------------------3FLD------------------------------
            [fs_FLD3_A,~,~,~]=FLD3_760(data_irrd,data_rad,fw);
            %---------------------------iFLD-------------------------------
            [fs_iFLD_A,~,~,~]=iFLD(data_irrd,data_rad,fw);
            %---------------------------eFLD-------------------------------
            [fs_eFLD_A,~]=eFLD(data_irrd,data_rad);
            %---------------------------SFM--------------------------------
            [fs_sfm_Aall,~,~,~]= SFM(data_irrd,data_rad);
            %--------------------------result------------------------------
            % ********************************************************************************************************************
            SIFA = [SIFA;Gnum,hour,mint,sec,time,Hs,fs_sFLD_A,fs_FLD3_A,fs_iFLD_A,fs_eFLD_A,fs_sfm_Aall] ;
            % ********************************************************************************************************************
            %% 大气校正sif
            obs_time=Hs_format_time/24;
            H=10-2;             obs_angle=90;
            sza=Hs;             Date=string_date;
            [irrad_cor,rad_cor,ref_cor]=atmos_cor(data_irrd(:,2),data_rad(:,2),wl',obs_time,H,obs_angle,sza,Date,Tem_press_all_data);
            data_irrd(:,2)=irrad_cor;
            data_rad(:,2)=rad_cor;
    %         ref=ref_cor;
            %----------------------------sFLD-------------------------------
            [fs_sFLD_A,TrueRef_A,fs_sFLD_B,TrueRef_B]=sFLD(data_irrd,data_rad,fw);
            %----------------------------3FLD------------------------------
            [fs_FLD3_A,TrueRef3A,fs_FLD3_B,TrueRef3B]=FLD3_760(data_irrd,data_rad,fw);
            %---------------------------iFLD-------------------------------
            [fs_iFLD_A,TrueRefiA,fs_iFLD_B,TrueRefiB]=iFLD(data_irrd,data_rad,fw);
            %---------------------------eFLD-------------------------------
            [fs_eFLD_A,fs_eFLD_B]=eFLD(data_irrd,data_rad);
            %---------------------------SFM--------------------------------
            [fs_sfm_Aall,trueref_sfm_Aall,fs_sfm_Ball,trueref_sfm_Ball]= SFM(data_irrd,data_rad);
            %--------------------------result------------------------------
            % ********************************************************************************************************************
            SIFAatc = [SIFAatc;Gnum,hour,mint,sec,time,Hs,fs_sFLD_A,fs_FLD3_A,fs_iFLD_A,fs_eFLD_A,fs_sfm_Aall] ;
            % ********************************************************************************************************************
        end
    end
    %% save SIF to txt file
    disp(['saving ' string_date ' sif file...']);
   
%     SIFA=sortrows(SIFA,1);	
    fileID = fopen([savepath '\' 'SIF_' string_date 'sifA.txt'],'w');
    for row =1:size(SIFA,1)
        if row ==1
            fprintf(fileID,'Number\tHour\tMinute\tSecond\ttime\tSolar_Altitude\tfs_sFLD_A\tfs_FLD3_A\tfs_iFLD_A\tfs_eFLD_A\tf_sfm_OLS\tfs_sfm_lin_lin\tfs_sfm_quad_lin\tfs_sfm_cubic_lin\tfs_sfm_gauss_lin\r\n');  
        end
        fprintf(fileID,'%d\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\r\n',SIFA(row,:));
    end
    fclose(fileID);
    % 
%     SIFAatc=sortrows(SIFAatc,1);	
    fileID = fopen([savepath1 '\' 'SIF_' string_date 'sifA.txt'],'w');
    for row =1:size(SIFAatc,1)
        if row ==1
            fprintf(fileID,'Number\tHour\tMinute\tSecond\ttime\tSolar_Altitude\tfs_sFLD_A\tfs_FLD3_A\tfs_iFLD_A\tfs_eFLD_A\tf_sfm_OLS\tfs_sfm_lin_lin\tfs_sfm_quad_lin\tfs_sfm_cubic_lin\tfs_sfm_gauss_lin\r\n');  
        end
        fprintf(fileID,'%d\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\r\n',SIFAatc(row,:));
    end
    fclose(fileID);
    
    disp(['saving ' string_date ' sif file completed...']);
end