clear;
clc;
addpath('D:\Data\Xilinhot2017 Code');
addpath('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab_code\atmos_correction');
% Oridata_path='D:\Data\shangqiu data\shang\';
Oridata_path='D:\Data\shangqiu data\shang\';
file_spec=dir([Oridata_path '2017*\']);
Qe_saturation_val=160000;
Hr_saturation_val=15000;  % 12000 seems too small?
datapro_savefoldername='Results_QEradiance_nocontrol_atmoscor';

%%------extract calibration file -----------
% remember to change filename once site changed 
Cal_path=[Oridata_path 'calibration data for calculate SIF\'];
qeDW_cal_filename='QEP01108地物.txt';
qeRZ_cal_filename='QE_RZ_LAMP.txt';
% qeRZ_cal_filename='QEP01108入照.txt';
hrDW_cal_filename='HR+D0784地物.txt';
hrRZ_cal_filename='HR+D0784入照.txt';
addpath(Cal_path);
% 温度，气压数据
Tem_press_all_data=xlsread('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab_code\atmos_correction\Tem_press_all_data.xlsx');

fid1=fopen(qeDW_cal_filename);
data=textscan(fid1,'%f%f','headerlines',6);
fclose(fid1);
Wavele=data{1,1};    %wavelength
Convert_index_qeDW=data{1,2};
Convert_index_qeDW=Convert_index_qeDW(5:end-4,1);

fid1=fopen(qeRZ_cal_filename);
data=textscan(fid1,'%f%f','headerlines',6);
fclose(fid1);
Convert_index_qeRZ=data{1,2};
Convert_index_qeRZ=Convert_index_qeRZ(5:end-4,1);  

fid1=fopen(hrDW_cal_filename);
data=textscan(fid1,'%f%f','headerlines',6);
fclose(fid1);
Convert_index_hrDW=data{1,2};
Convert_index_hrDW=Convert_index_hrDW(5:end-4,1);

fid1=fopen(hrRZ_cal_filename);
data=textscan(fid1,'%f%f','headerlines',6);
fclose(fid1);
Convert_index_hrRZ=data{1,2};
Convert_index_hrRZ=Convert_index_hrRZ(5:end-4,1)/10;
for i=61:length(file_spec)
    disp([file_spec(i).name ' is processing...']);
    
    Auto_path=[Oridata_path file_spec(i).name '\Auto\'];
	QE_path=[Auto_path 'QEP01108'];
	HR_path=[Auto_path 'HR+D0784'];
	QEfile=dir([QE_path '\G*.txt']);
	HRfile=dir([HR_path '\G*.txt']);
	
	if ~exist([Oridata_path datapro_savefoldername '\SIF_QE'],'dir')
		mkdir([Oridata_path datapro_savefoldername '\SIF_QE']);
	end
	if ~exist([Oridata_path datapro_savefoldername '\VI_HR'],'dir')
		mkdir([Oridata_path datapro_savefoldername '\VI_HR']);
    end
    if ~exist([Oridata_path datapro_savefoldername '\REF\QE_REF'],'dir')
		mkdir([Oridata_path datapro_savefoldername '\REF\QE_REF']);
    end
    if ~exist([Oridata_path datapro_savefoldername '\REF\HR_REF'],'dir')
		mkdir([Oridata_path datapro_savefoldername '\REF\HR_REF']);
	end
	if ~exist([Oridata_path datapro_savefoldername '\Radiance\QE\Irradiance'],'dir')
		mkdir([Oridata_path datapro_savefoldername '\Radiance\QE\Irradiance']);
    end
    if ~exist([Oridata_path datapro_savefoldername '\Radiance\QE\Radiance'],'dir')
		mkdir([Oridata_path datapro_savefoldername '\Radiance\QE\Radiance']);
    end
    if ~exist([Oridata_path datapro_savefoldername '\Radiance\HR\Irradiance'],'dir')
		mkdir([Oridata_path datapro_savefoldername '\Radiance\HR\Irradiance']);
    end
    if ~exist([Oridata_path datapro_savefoldername '\Radiance\HR\Radiance'],'dir')
		mkdir([Oridata_path datapro_savefoldername '\Radiance\HR\Radiance']);
    end
	
    SIFA=[];
    SIFB=[];
	count=1;
    count1=1;
    VeIndex=[];
    QEREF=[];
    HRREF=[];
    QEIRRADIANCE=[];
    QERADIANCE=[];  
    HRIRRADIANCE=[];
    HRRADIANCE=[];
	%% -------QE ,to get sif and reflectance ---------------------
	for j=1:3:length(QEfile)
		filename=QEfile(j).name;
        addpath(QE_path);
		str=filename;
		temp_=find(str=='_');
		before_=str(1:temp_(1)-1);
		after_=str(temp_(1)+1:end);
		%%-----------Eg1-----------------
		fid=fopen(filename);
		data=textscan(fid,'%f%f%f%f','headerlines',18);
		fclose(fid);
		fid=fopen(filename);
		tline=textscan(fid,'%s','headerlines',6,'delimiter','\t');
		fclose(fid);
		Wavelength=data{1,1};
		Wavelength=Wavelength(5:end-4,1);
		Eg1=data{1,2};
%         if ~isempty(Eg1)    % 排除没有数据的情况
        Eg1=Eg1(5:end-4,1);
        Eg1_DC=data{1,3};
        Eg1_DC=Eg1_DC(5:end-4,1);
        IRRidiance1=data{1,4};
        IRRidiance1=IRRidiance1(5:end-4,1);

        % get inttime 
        inttime=str2num(tline{1,1}{2,1});
        % get date 
        fid=fopen(filename);
        starttime=textscan(fid,'%s','headerlines',10,'delimiter','\t');
        fclose(fid);
        Start_time=starttime{1,1}{2,1};
        tep=find(Start_time==':');
        space=find(Start_time==' ');
        hour=Start_time(space(1)+1:tep(1)-1);
        inthour=str2num(hour);
        clocktime=Start_time(space(1)+1:end);
        % *****************************************************************************************
        time=datenum(Start_time);
        % ****************************************************************************************
        % 'hour:min:sec'to 'hour min sec'
        mint=Start_time(tep(1)+1:tep(2)-1);
        sec=Start_time(tep(2)+1:end);
        Clocktime=[hour,' ', mint ,' ',sec];

        if(inthour<6 || inthour>18)
            continue;
        else
            %%-------------Ls-----------------
            fid=fopen(QEfile(j+1).name);
            data=textscan(fid,'%f%f%f%f','headerlines',18);
            fclose(fid);
            fid=fopen(QEfile(j+1).name);
            tlinels=textscan(fid,'%s','headerlines',6,'delimiter','\t');
            fclose(fid);

            Ls=data{1,2};
            Ls=Ls(5:end-4,1);
            Ls_DC=data{1,3};
            Ls_DC=Ls_DC(5:end-4,1);
            Ridiance=data{1,4};
            Ridiance=Ridiance(5:end-4,1);

            % get inttime
            inttime2=str2num(tlinels{1,1}{2,1});
            %%--------------Eg2--------------------
            fid=fopen(QEfile(j+2).name);
            data=textscan(fid,'%f%f%f%f','headerlines',18);
            fclose(fid);
            fid=fopen(QEfile(j+2).name);
            tlineeg2=textscan(fid,'%s','headerlines',6,'delimiter','\t');
            fclose(fid);

            Eg2=data{1,2};
            Eg2=Eg2(5:end-4,1);
            Eg2_DC=data{1,3};
            Eg2_DC=Eg2_DC(5:end-4,1);
            IRRidiance2=data{1,4};
            IRRidiance2=IRRidiance2(5:end-4,1);

            % get inttime
            inttime3=str2num(tlineeg2{1,1}{2,1});
            % average for Irradiance
            IRRidiance=(IRRidiance1+IRRidiance2)/2;
            
          %% -----Irradiance and radiance data quality control----
            %DQsza

            %DQsat

            Eg=(Eg1+Eg2)/2;
            DC=(Eg1_DC+Eg2_DC)/2;
            DC=mean(DC);
            % before 20171008 use this  //criteria 1
% 			if(max(Eg1)>Qe_saturation_val || max(Eg2)>Qe_saturation_val || max(abs(Eg1-Eg2))*100/min(Eg1)<0.1...
% 			|| min(pi*Ls)/max(Eg*100)>1 || min(Eg)/(DC*100)>0.3 || max(Eg)<0.5*Qe_saturation_val )
            % 20171008 use this  //criteria 2
%              if(max(Eg1)>Qe_saturation_val || max(Eg2)>Qe_saturation_val || max(abs(Eg1-Eg2))/min(Eg1)>0.1...
% 			|| min(pi*Ls)/max(Eg)>1 || min(Eg)/(DC*100)>0.3 || max(Eg)<0.5*Qe_saturation_val...
%             || max(Eg1)<0.5*Qe_saturation_val || max(Eg2)<0.5*Qe_saturation_val ...
%             || max(abs(Eg1-Eg2)./Eg1)>0.02 || max(abs(Eg1-Eg2)./Eg2)>0.02 )
            % 20171013 use this  //criteria 3
%              if(max(Eg1)>Qe_saturation_val || max(Eg2)>Qe_saturation_val || max(abs(Eg1-Eg2)./Eg)>0.1...
% 			|| min(pi*Ls)/max(Eg)>1 || min(Eg)/(DC*100)>0.3 || max(Eg)<0.5*Qe_saturation_val...
%             || max(Eg1)<0.5*Qe_saturation_val || max(Eg2)<0.5*Qe_saturation_val)
             % 20171013 use this  //criteria 4 (best choice)
            %% -----------wrong !-------------------
%             if(max(Eg1)>Qe_saturation_val || max(Eg2)>Qe_saturation_val || max(abs(Eg1-Eg2))/min(Eg1)>0.1...
%             || min(pi*Ls)/max(Eg)>1 || min(Eg)/(DC*100)>0.3 || max(Eg)<0.5*Qe_saturation_val...
%             || max(Eg1)<0.5*Qe_saturation_val || max(Eg2)<0.5*Qe_saturation_val)
            %% -------------------------------------
            %20180712
%             if(max(Eg1)>Qe_saturation_val || max(Eg2)>Qe_saturation_val || max(abs(Eg1-Eg2))/min(Eg1)>0.1...
%             || min(pi*Ls)/max(Eg)>1 || min(Eg(5:end-4,1))/DC<0.3 || max(Eg)<0.5*Qe_saturation_val...
%             || max(Eg1)<0.5*Qe_saturation_val || max(Eg2)<0.5*Qe_saturation_val)
%                 Eg1=nan;
%                 Ls=nan;
%                 Eg2=nan;
%             end
            %% 20181027
            if(max(Eg1)>Qe_saturation_val || max(Eg2)>Qe_saturation_val)
                Eg1=nan;
                Ls=nan;
                Eg2=nan;
            end
            %%

            Eg1_DN=Eg1-Eg1_DC;
            Ls_DN=Ls-Ls_DC;
            Eg2_DN=Eg2-Eg2_DC;

          %% ----------nonlinear correction-----------------------
            %for Eg1
            p_qe = [-2.7053e-37,1.6867e-31,-4.15473e-26,5.11313e-21,...
            -3.26716e-16,9.22e-12,2.55346e-8,0.994225];

% 			Fp=-7.1499e-35*Eg1_DN+1.44288e-29*Eg1_DN+-1.17819e-24*Eg1_DN+4.89779e-20*Eg1_DN+...
% 				 -9.59158e-16*Eg1_DN+-1.19536e-11*Eg1_DN+1.30382e-6*Eg1_DN+0.976;

            Fp = polyval(p_qe,Eg1_DN(:,1));
            Rp = Eg1_DN./Fp;
            IRRAD_Eg1_DN=Rp/inttime;

            % % for Ls 
% 			Fpls=-7.1499e-35*Ls_DN+1.44288e-29*Ls_DN+-1.17819e-24*Ls_DN+4.89779e-20*Ls_DN+...
% 				-9.59158e-16*Ls_DN+-1.19536e-11*Ls_DN+1.30382e-6*Ls_DN+0.976;
            Fpls=polyval(p_qe,Ls_DN(:,1));
            Rpls=Ls_DN./Fpls;
            RAD_Ls_DN=Rpls/inttime2;

            % %for Eg2
% 			Fp=-7.1499e-35*Eg2_DN+1.44288e-29*Eg2_DN+-1.17819e-24*Eg2_DN+4.89779e-20*Eg2_DN+...
% 				-9.59158e-16*Eg2_DN+-1.19536e-11*Eg2_DN+1.30382e-6*Eg2_DN+0.976;
            Fp = polyval(p_qe,Eg2_DN(:,1));
            Rp = Eg2_DN./Fp;
            IRRAD_Eg2_DN=Rp/inttime3;

            %************************************************

            %% transfer DN to Irradiance & radiance
            RAD=RAD_Ls_DN.*Convert_index_qeDW;
            IRRAD1=IRRAD_Eg1_DN.*Convert_index_qeRZ;
            IRRAD2=IRRAD_Eg2_DN.*Convert_index_qeRZ;
            %--------------------------solar altitude------------------------------
            string_date=file_spec(i).name;
            Hs_format_time=str2num(hour)+str2num(mint)/60+str2num(sec)/3600;
            Hs=Solar_Altitude(115.5916,34.5199,string_date,Hs_format_time);
            %----------------------------------------------------
            data_irrd1=[Wavelength IRRAD1];  
            data_rad=[Wavelength RAD];
            data_irrd2=[Wavelength IRRAD2];
            data_irrd=(data_irrd1+data_irrd2)./2; 
            
            ref=pi*data_rad(:,2)./data_irrd(:,2);
            % --------------------sif calculate------------------
            str=filename;
            temp_=find(str=='_');
            space=find(str==' ');
            % tempG=find(str=='G');
            before_=str(2:temp_(1)-1);
            % hour=str(temp_(2)+1:space(1)-1);
            % mint=str(space(1)+1:space(2)-1);
            % sec=str(space(2)+1:end-4);
            clocktime=[hour,':',mint,':',sec];
            % after_=str(temp_(1)+1:end);
            Gnum=str2num(before_);  
            
            % *************************************************************************************************************
            if(min(isnan(data_irrd(:,2)))==1 || min(isnan(data_rad(:,2))==1) || max(data_irrd(:,2))==0)%|| max(pi*data_rad(:,2)./data_irrd(:,2))>0.5)
                SIFA(count,1:6)=[Gnum,str2num(hour),str2num(mint),str2num(sec),time,Hs];
                SIFA(count,7:15)=nan;
                SIFB(count,1:6)=[Gnum,str2num(hour),str2num(mint),str2num(sec),time,Hs];
                SIFB(count,7:15)=nan;
                count=count+1;
                %----------------------------- ref & radiance----------------------------
                QEREF=[QEREF;Gnum,str2num(hour),str2num(mint),str2num(sec),time,ref'];
                QEIRRADIANCE=[QEIRRADIANCE;Gnum,str2num(hour),str2num(mint),str2num(sec),time,data_irrd(:,2)'];
                QERADIANCE=[QERADIANCE;Gnum,str2num(hour),str2num(mint),str2num(sec),time,data_rad(:,2)'];  
                continue;
            % *************************************************************************************************************
            else
              %% 大气校正（ref Liu et al., 2019）
                wl=Wavelength;      obs_time=Hs_format_time/24;
                H=10-2;             obs_angle=90;
                sza=Hs;             Date=file_spec(i).name;
                [irrad_cor,rad_cor,ref_cor]=atmos_cor(data_irrd(:,2),data_rad(:,2),wl,obs_time,H,obs_angle,sza,Date,Tem_press_all_data);
                data_irrd(:,2)=irrad_cor;
                data_rad(:,2)=rad_cor;
                ref=ref_cor;
                %----------------------------- ref & radiance----------------------------
                QEREF=[QEREF;Gnum,str2num(hour),str2num(mint),str2num(sec),time,ref'];
                QEIRRADIANCE=[QEIRRADIANCE;Gnum,str2num(hour),str2num(mint),str2num(sec),time,data_irrd(:,2)'];
                QERADIANCE=[QERADIANCE;Gnum,str2num(hour),str2num(mint),str2num(sec),time,data_rad(:,2)'];  
%               %% 20171011 added , fwhm=0.0667*3 =0.2001-->about 0.2
%                 fw=0.2;
%                 %----------------------------sFLD-------------------------------
%                 [fs_sFLD_A,TrueRef_A,fs_sFLD_B,TrueRef_B]=sFLD(data_irrd,data_rad,fw);
%                 %----------------------------3FLD------------------------------
%                 [fs_FLD3_A,TrueRef3A,fs_FLD3_B,TrueRef3B]=FLD3_760(data_irrd,data_rad,fw);
% 
%                 %************************from papers*************************************
%                 %---------------------------cFLD-------------------------------
%                 % ref: G贸mez-Chova et al. (2006) and Moya et al. (2006)
% 
%                 % r(lamda_in)=alpha_r * r(lamda_out);
%                 % F(lamda_in)=alpha_F * F(lamda_out);
%                 % in which,alpha_r can be deduced from apparent reflectance by interpolating the values ...
%                 % obtained outside of the absortation feature; while alpha_F is instead deduced from ...
%                 % dedicated measurements of actual F at the leaf level. 
% 
%                 %---------------------------iFLD-------------------------------
%                 [fs_iFLD_A,TrueRefiA,fs_iFLD_B,TrueRefiB]=iFLD(data_irrd,data_rad,fw);
%                 %---------------------------eFLD-------------------------------
% %                 [fs_eFLD_A,fs_eFLD_B]=eFLD(data_irrd,data_rad);
%                 fs_eFLD_A=nan;fs_eFLD_B=nan;
%                 %---------------------------SFM--------------------------------
%                 [fs_sfm_Aall,trueref_sfm_Aall,fs_sfm_Ball,trueref_sfm_Ball]= SFM_760(data_irrd,data_rad);
% 
%                 %--------------------------result------------------------------
%                 % ********************************************************************************************************************
%                 SIFA(count,:) = [Gnum,str2num(hour),str2num(mint),str2num(sec),time,Hs,fs_sFLD_A,fs_FLD3_A,fs_iFLD_A,fs_eFLD_A,fs_sfm_Aall] ;
%                 SIFB(count,:) = [Gnum,str2num(hour),str2num(mint),str2num(sec),time,Hs,fs_sFLD_B,fs_FLD3_B,fs_iFLD_B,fs_eFLD_B,fs_sfm_Ball] ;
%                 % ********************************************************************************************************************
%                 count=count+1;
            end
        end 
%         end
    end
   %% ***************************2017.12.22 change by Lzh********************************
   %% save ref to xlsx file
    QEREF1=sortrows(QEREF,1);
    IRRADIANCE1=sortrows(QEIRRADIANCE,1);
    RADIANCE1=sortrows(QERADIANCE,1);
    disp(['writing qe' file_spec(i).name ' xlsx file']);
    title={'Number','hour','min','sec','time'};
    xlswrite([Oridata_path datapro_savefoldername '\REF\QE_REF\ref_' file_spec(i).name '.xlsx'],title,1,'A1');
    xlswrite([Oridata_path datapro_savefoldername '\REF\QE_REF\ref_' file_spec(i).name '.xlsx'],Wavelength',1,'F1');
    xlswrite([Oridata_path datapro_savefoldername '\REF\QE_REF\ref_' file_spec(i).name '.xlsx'],QEREF1,1,'A2');
    xlswrite([Oridata_path datapro_savefoldername '\Radiance\QE\Irradiance\' file_spec(i).name '_irradiance.xlsx'],title,1,'A1');
    xlswrite([Oridata_path datapro_savefoldername '\Radiance\QE\Irradiance\' file_spec(i).name '_irradiance.xlsx'],Wavelength',1,'F1');
    xlswrite([Oridata_path datapro_savefoldername '\Radiance\QE\Irradiance\' file_spec(i).name '_irradiance.xlsx'],IRRADIANCE1,1,'A2');
    xlswrite([Oridata_path datapro_savefoldername '\Radiance\QE\Radiance\' file_spec(i).name '_radiance.xlsx'],title,1,'A1');
    xlswrite([Oridata_path datapro_savefoldername '\Radiance\QE\Radiance\' file_spec(i).name '_radiance.xlsx'],Wavelength',1,'F1');
    xlswrite([Oridata_path datapro_savefoldername '\Radiance\QE\Radiance\' file_spec(i).name '_radiance.xlsx'],RADIANCE1,1,'A2');
    disp([file_spec(i).name 'qe is ok']);
    
%     %% save SIF to txt file
%     SIFA=sortrows(SIFA,1);	
%     fileID = fopen([Oridata_path datapro_savefoldername '\SIF_QE' '\' 'SIF_' file_spec(i).name 'sifA.txt'],'w');
%     for row =1:size(SIFA,1)
%         if row ==1
%             fprintf(fileID,'Number\tHour\tMinute\tSecond\ttime\tSolar_Altitude\tfs_sFLD_A\tfs_FLD3_A\tfs_iFLD_A\tfs_eFLD_A\tf_sfm_OLS\tfs_sfm_lin_lin\tfs_sfm_quad_lin\tfs_sfm_cubic_lin\tfs_sfm_gauss_lin\r\n');  
%         end
%         fprintf(fileID,'%d\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\r\n',SIFA(row,:));
%     end
%     fclose(fileID); 
%     % plot SIF
% % regardless of solar altitude
%     SIFB=sortrows(SIFB,1);
%     fileID = fopen([Oridata_path datapro_savefoldername '\SIF_QE' '\' 'SIF_' file_spec(i).name 'sifB.txt'],'w');
%     for row =1:size(SIFB,1)
%         if row ==1
%             fprintf(fileID,'Number\tHour\tMinute\tSecond\ttime\tSolar_Altitude\tfs_sFLD_B\tfs_FLD3_B\tfs_iFLD_B\tfs_eFLD_B\tf_sfm_OLSB\tfs_sfm_lin_linB\tfs_sfm_quad_linB\tfs_sfm_cubic_linB\tfs_sfm_gauss_linB\r\n');  
%         end
%         fprintf(fileID,'%d\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\r\n',SIFB(row,:));
%     end
%     fclose(fileID);




     %*************************************************************************************************
%      % save SIF to txt file
%   %  regardless of solar altitude
%     if ~isempty(SIFA)
%         SIFA=sortrows(SIFA,1);	
%         if(min(isnan(SIFA(:,6:end)))~=1)   
%             fileID = fopen([Oridata_path datapro_savefoldername '\SIF_QE' '\' 'temp' file_spec(i).name 'sifA.txt'],'w');
%             for row =1:size(SIFA,1)
%                 if row ==1
%                     fprintf(fileID,'Number\tHour\tMinute\tSecond\ttime\tSolar_Altitude\tfs_sFLD_A\tfs_FLD3_A\tfs_iFLD_A\tfs_eFLD_A\tf_sfm_OLS\tfs_sfm_lin_lin\tfs_sfm_quad_lin\tfs_sfm_cubic_lin\tfs_sfm_gauss_lin\r\n');  
%                 end
%                 fprintf(fileID,'%d\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\r\n',SIFA(row,:));
%             end
%             fclose(fileID); 
%             % plot SIF
%             savepath=[Oridata_path datapro_savefoldername '\SIF_QE'];
%             ShowSIFA(SIFA,file_spec(i).name,savepath);
%         end
%         % take solar altitude into consideration
%         SIFA(SIFA(:,5)>60,6:end)=nan;
%         if(min(isnan(SIFA(:,6:end)))~=1)   
%             savepath=[Oridata_path datapro_savefoldername '\SIF_QE'];
%             ShowSIFA(SIFA,['Solar Altitude' file_spec(i).name],savepath);
%         end
%     end
%     % only valid data exists in SIFB can SIFB be showed 
%     % regardless of solar altitude
%     if ~isempty(SIFB)
%         SIFB=sortrows(SIFB,1);
%         if(min(isnan(SIFB(:,6:end)))~=1)   	
%             fileID = fopen([Oridata_path datapro_savefoldername '\SIF_QE' '\' 'temp' file_spec(i).name 'sifB.txt'],'w');
%             for row =1:size(SIFB,1)
%                 if row ==1
%                     fprintf(fileID,'Number\tHour\tMinute\tSecond\ttime\tSolar_Altitude\tfs_sFLD_B\tfs_FLD3_B\tfs_iFLD_B\tfs_eFLD_B\tf_sfm_OLSB\tfs_sfm_lin_linB\tfs_sfm_quad_linB\tfs_sfm_cubic_linB\tfs_sfm_gauss_linB\r\n');  
%                 end
%                 fprintf(fileID,'%d\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\r\n',SIFB(row,:));
%             end
%             fclose(fileID);
%             % plot SIF
%             ShowSIFB(SIFB,file_spec(i).name,savepath);
%         end
%         % take solar altitude into consideration
%         SIFB(SIFB(:,5)>60,6:end)=nan;
%         if(min(isnan(SIFB(:,6:end)))~=1)   
%             savepath=[Oridata_path datapro_savefoldername '\SIF_QE'];
%             ShowSIFB(SIFA,['Solar Altitude' file_spec(i).name],savepath);
%         end
%     end
%     %% -------------------------HR--------------------------------
%     for j=1:3:length(HRfile)
% 		filename=HRfile(j).name;
% 		addpath(HR_path);
% 		str=filename;
% 		temp_=find(str=='_');
% 		before_=str(1:temp_(1)-1);
% 		after_=str(temp_(1)+1:end);
% 		%%-----------Eg1-----------------
% 		fid=fopen(filename);
% 		data=textscan(fid,'%f%f%f%f','headerlines',18);
% 		fclose(fid);
% 		fid=fopen(filename);
% 		tline=textscan(fid,'%s','headerlines',6,'delimiter','\t');
% 		fclose(fid);
% 		Wavelength=data{1,1};
% 		Wavelength=Wavelength(5:end-4,1);
% 		Eg1=data{1,2};
% 		Eg1=Eg1(5:end-4,1);
% 		Eg1_DC=data{1,3};
% 		Eg1_DC=Eg1_DC(5:end-4,1);
% 		IRRidiance1=data{1,4};
% 		IRRidiance1=IRRidiance1(5:end-4,1);
% 		
% 		% get inttime 
% 		inttime=str2num(tline{1,1}{2,1});
% 		% get date 
% 		fid=fopen(filename);
% 		starttime=textscan(fid,'%s','headerlines',10,'delimiter','\t');
% 		fclose(fid);
% 		Start_time=starttime{1,1}{2,1};
% 		tep=find(Start_time==':');
% 		space=find(Start_time==' ');
% 		hour=Start_time(space(1)+1:tep(1)-1);
% 		inthour=str2num(hour);
% 		clocktime=Start_time(space(1)+1:end);
%         % ***********************************************************************************************
% 		time=datenum(Start_time);
%         % ***********************************************************************************************
% 		% 'hour:min:sec'to 'hour min sec'
% 		mint=Start_time(tep(1)+1:tep(2)-1);
% 		sec=Start_time(tep(2)+1:end);
% 		Clocktime=[hour,' ', mint ,' ',sec];
% 
% 		if(inthour<6 || inthour>18)
% 			continue;
% 		else
% 			%%-------------Ls-----------------
% 			fid=fopen(HRfile(j+1).name);
% 			data=textscan(fid,'%f%f%f%f','headerlines',18);
% 			fclose(fid);
% 			fid=fopen(HRfile(j+1).name);
% 			tlinels=textscan(fid,'%s','headerlines',6,'delimiter','\t');
% 			fclose(fid);
% 
% 			Ls=data{1,2};
% 			Ls=Ls(5:end-4,1);
% 			Ls_DC=data{1,3};
% 			Ls_DC=Ls_DC(5:end-4,1);
% 			Ridiance=data{1,4};
% 			Ridiance=Ridiance(5:end-4,1);
% 			
% 			% get inttime
% 			inttime2=str2num(tlinels{1,1}{2,1});
% 			%%--------------Eg2--------------------
% 			fid=fopen(HRfile(j+2).name);
% 			data=textscan(fid,'%f%f%f%f','headerlines',18);
% 			fclose(fid);
% 			fid=fopen(HRfile(j+2).name);
% 			tlineeg2=textscan(fid,'%s','headerlines',6,'delimiter','\t');
% 			fclose(fid);
% 
% 			Eg2=data{1,2};
% 			Eg2=Eg2(5:end-4,1);
% 			Eg2_DC=data{1,3};
% 			Eg2_DC=Eg2_DC(5:end-4,1);
% 			IRRidiance2=data{1,4};
% 			IRRidiance2=IRRidiance2(5:end-4,1);
% 			
% 			% get inttime
% 			inttime3=str2num(tlineeg2{1,1}{2,1});
% 			% average for Irradiance
% 			IRRidiance=(IRRidiance1+IRRidiance2)/2;
% 			%------------Irradiance and radiance data quality control--------------------
% 			%DQsza
% 				
% 			%DQsat
% 				
% % 			Eg=(Eg1+Eg2)/2;
% % 			DC=(Eg1_DC+Eg2_DC)/2;
% % 			DC=mean(DC);
% % 
% %             if(max(Eg1)>Hr_saturation_val || max(Eg2)>Hr_saturation_val || min(Eg(561:1475,1))/DC<0.3...
% %                 || max(Eg1)<0.5*Hr_saturation_val || max(Eg2)<0.5*Hr_saturation_val )
% % 				Eg1=nan;
% % 				Ls=nan;
% % 				Eg2=nan;
% % 			end
% 
% 			Eg1_DN=Eg1-Eg1_DC;
% 			Ls_DN=Ls-Ls_DC;
% 			Eg2_DN=Eg2-Eg2_DC;
%             
%             
% 			% nonlinear correction
% 			%*******************************************
% 			% %for Eg1
% % 			p_qe = [2.22818e-29,-1.3233e-24,2.93682e-20,-3.18976e-16,1.82476e-12,-6.05169e-9,2.10855e-5,0.92248];
% 				
% % 			Fp=-7.1499e-35*Eg1_DN+1.44288e-29*Eg1_DN+-1.17819e-24*Eg1_DN+4.89779e-20*Eg1_DN+...
% % 				 -9.59158e-16*Eg1_DN+-1.19536e-11*Eg1_DN+1.30382e-6*Eg1_DN+0.976;
% 				
% % 			Fp = polyval(p_qe,Eg1_DN(:,1));
% % 			Rp = Eg1_DN./Fp;
% 			IRRAD_Eg1_DN=Eg1_DN/inttime;
% 						
% 			% % for Ls 
% % 			Fpls=-7.1499e-35*Ls_DN+1.44288e-29*Ls_DN+-1.17819e-24*Ls_DN+4.89779e-20*Ls_DN+...
% % 				-9.59158e-16*Ls_DN+-1.19536e-11*Ls_DN+1.30382e-6*Ls_DN+0.976;
% % 			Fpls=polyval(p_qe,Ls_DN(:,1));
% % 			Rpls=Ls_DN./Fpls;
% 			RAD_Ls_DN=Ls_DN/inttime2;
% 					
% 			% %for Eg2
% % 			Fp=-7.1499e-35*Eg2_DN+1.44288e-29*Eg2_DN+-1.17819e-24*Eg2_DN+4.89779e-20*Eg2_DN+...
% % 				-9.59158e-16*Eg2_DN+-1.19536e-11*Eg2_DN+1.30382e-6*Eg2_DN+0.976;
% % 			Fp = polyval(p_qe,Eg2_DN(:,1));
% % 			Rp = Eg2_DN./Fp;
% 			IRRAD_Eg2_DN=Eg2_DN/inttime3;
% 					
% 			%************************************************
% 				
%             %% transfer DN to Irradiance & radiance
% 			RAD=RAD_Ls_DN.*Convert_index_hrDW;
% 			IRRAD1=IRRAD_Eg1_DN.*Convert_index_hrRZ;
% 			IRRAD2=IRRAD_Eg2_DN.*Convert_index_hrRZ;
% 			%----------------------------------------------------
% 			data_irrd1=[Wavelength IRRAD1];  
% 			data_rad=[Wavelength RAD];
% 			data_irrd2=[Wavelength IRRAD2];
% 			data_irrd=(data_irrd1+data_irrd2)./2; 
%             
% 			ref=data_rad(:,2)./data_irrd(:,2);
%           %% --------------------sif calculate ------------------
%             % get num
% 			str=filename;
% 			temp_=find(str=='_');
% 			space=find(str==' ');
% 			% tempG=find(str=='G');
% 			before_=str(2:temp_(1)-1);
% 			% hour=str(temp_(2)+1:space(1)-1);
% 			% mint=str(space(1)+1:space(2)-1);
% 			% sec=str(space(2)+1:end-4);
% 			clocktime=[hour,':',mint,':',sec];
% 			% after_=str(temp_(1)+1:end);
% 			Gnum=str2num(before_);
% 			%--------------------------solar altitude----------------------
%             string_date=file_spec(i).name;
%             Hs_format_time=str2num(hour)+str2num(mint)/60+str2num(sec)/3600;
%             Hs=Solar_Altitude(116,44,string_date,Hs_format_time);
%             %--------------------------------------------------------------  
% %             DN_Irradiance=[DN_Irradiance;Gnum,str2num(hour),str2num(mint),str2num(sec),time-693960,(IRRAD_Eg1_DN+IRRAD_Eg2_DN)'/2];
% %             DN_radiance=[DN_radiance;Gnum,str2num(hour),str2num(mint),str2num(sec),time-693960,RAD_Ls_DN'];
%             
%             HRREF=[HRREF;Gnum,str2num(hour),str2num(mint),str2num(sec),time,ref'];
%             HRIRRADIANCE=[HRIRRADIANCE;Gnum,str2num(hour),str2num(mint),str2num(sec),time,data_irrd(:,2)'];
%             HRRADIANCE=[HRRADIANCE;Gnum,str2num(hour),str2num(mint),str2num(sec),time,data_rad(:,2)'];  
%             % **************************************************************************************************
% 			if(min(isnan(data_irrd(:,2)))==1 || min(isnan(data_rad(:,2))==1) )%|| max(pi*data_rad(:,2)./data_irrd(:,2))>0.5 )
% 				VeIndex(count1,1:6)=[Gnum,str2num(hour),str2num(mint),str2num(sec),time,Hs];
%                 VeIndex(count1,7:16)=nan;
%                 count1=count1+1;
% 				continue; 
% 			else
%               %% VI calculate
%                 [EVIsim,NDVIsim,MTCIsim,PRI,GreenNDVI,RedEdgeNDVI,CIgreen,CI705,CI740,SR] = calculate_simulatedVI(Wavelength/1000,ref);
%                 VeIndex(count1,:)=[Gnum,str2num(hour),str2num(mint),str2num(sec),time,Hs,EVIsim,NDVIsim,MTCIsim,PRI,GreenNDVI,RedEdgeNDVI,CIgreen,CI705,CI740,SR];
%                 count1=count1+1;
%             end
%             % **************************************************************************************************
%         end 
%     end 
%     %% save ref to xlsx file  
% %     IRRADIANCE1=sortrows(DN_Irradiance,1);
% %     RADIANCE1=sortrows(DN_radiance,1);
% %     disp(['writing ' file_spec(i).name ' xlsx file']);
% %     title={'Number','hour','min','sec','time'};
% %     xlswrite([Oridata_path datapro_savefoldername '\DN\' file_spec(i).name '_IrDN.xlsx'],title,1,'A1');
% %     xlswrite([Oridata_path datapro_savefoldername '\DN\' file_spec(i).name '_IrDN.xlsx'],Wavelength',1,'F1');
% %     xlswrite([Oridata_path datapro_savefoldername '\DN\' file_spec(i).name '_IrDN.xlsx'],IRRADIANCE1,1,'A2');
% %     disp([file_spec(i).name ' is ok']);
%     
%     HRREF1=sortrows(HRREF,1);
%     IRRADIANCE1=sortrows(HRIRRADIANCE,1);
%     RADIANCE1=sortrows(HRRADIANCE,1);
%     disp(['writing hr' file_spec(i).name ' xlsx file']);
%     title={'Number','hour','min','sec','time'};
%     xlswrite([Oridata_path datapro_savefoldername '\REF\HR_REF\ref_' file_spec(i).name '.xlsx'],title,1,'A1');
%     xlswrite([Oridata_path datapro_savefoldername '\REF\HR_REF\ref_' file_spec(i).name '.xlsx'],Wavelength',1,'F1');
%     xlswrite([Oridata_path datapro_savefoldername '\REF\HR_REF\ref_' file_spec(i).name '.xlsx'],HRREF1,1,'A2');
%     xlswrite([Oridata_path datapro_savefoldername '\Radiance\HR\Irradiance\' file_spec(i).name '_irradiance.xlsx'],title,1,'A1');
%     xlswrite([Oridata_path datapro_savefoldername '\Radiance\HR\Irradiance\' file_spec(i).name '_irradiance.xlsx'],Wavelength',1,'F1');
%     xlswrite([Oridata_path datapro_savefoldername '\Radiance\HR\Irradiance\' file_spec(i).name '_irradiance.xlsx'],IRRADIANCE1,1,'A2');
%     xlswrite([Oridata_path datapro_savefoldername '\Radiance\HR\Radiance\' file_spec(i).name '_radiance.xlsx'],title,1,'A1');
%     xlswrite([Oridata_path datapro_savefoldername '\Radiance\HR\Radiance\' file_spec(i).name '_radiance.xlsx'],Wavelength',1,'F1');
%     xlswrite([Oridata_path datapro_savefoldername '\Radiance\HR\Radiance\' file_spec(i).name '_radiance.xlsx'],RADIANCE1,1,'A2');
%     disp([file_spec(i).name 'hr is ok']);
%     %% save VI to txt file
%     % regardless of solar altitude
%     VeIndex=sortrows(VeIndex,1); 
%     fileID = fopen([Oridata_path datapro_savefoldername '\VI_HR' '\' 'VIs_' file_spec(i).name '.txt'],'w');
%     for row =1:size(VeIndex,1)
%         if row ==1
%             fprintf(fileID,'Number\tHour\tMinute\tSecond\ttime\tSolar_Altitude\tEVI\tNDVI\tMTCI\tPRI\tGreenNDVI\tRedEdgeNDVI\tCIgreen\tCI705\tCI740\tSR\r\n');  
%         end
%         fprintf(fileID,'%d\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\r\n',VeIndex(row,:));
%     end
%     fclose(fileID); 
end