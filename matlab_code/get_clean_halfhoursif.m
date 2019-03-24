clear;clc;

sifpath='D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\SIF_QE';
%% 先保存到一个excel中
filessif=dir([sifpath '\*sifA.txt']);
SIF=[];
for i=1:length(filessif)
    % get the date of the file
%     str=filessif(i).name;
%     Year=str(5:8);
%     Month=str(9:10);
%     Day=str(11:12);
    filename = [sifpath '\' filessif(i).name];
    data = importdata(filename);
    
    sif=data.data;
    text=data.textdata;
    SIF=[SIF;sif];
end
SIF(SIF<0)=nan;
xlswrite('D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\SIF_QE_all.xlsx',text,1,'A1');
xlswrite('D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\SIF_QE_all.xlsx',SIF,1,'A2');
%% 数据清洗，去掉异常值
hour=SIF(:,2);
time=SIF(:,5);
doy1=fix(SIF(1,5))-datenum(2017,1,1)+1;
doy2=fix(SIF(end,5))-datenum(2017,1,1)+1;
doy=time-datenum(2017,1,1)+1;

newdata=[];
halfhour=[];
for d=doy1:doy2
    for h=(9:0.5:16)/24
        t1=d+h-0.5/24;t2=d+h;
        idx=doy>=t1 & doy<t2;
        datat=SIF(idx,5);
        dataifldsif=SIF(idx,9);
        datasfmsif=SIF(idx,12);
        stdifld=nanstd(dataifldsif);
        stdsfm=nanstd(datasfmsif);
        % 去掉异常值(>3sigma or <-3sigma)
        dataifldsif(dataifldsif>3*stdifld | dataifldsif<-3*stdifld )=nan;
        datasfmsif(datasfmsif>3*stdsfm | datasfmsif<-3*stdsfm )=nan;
        % 半小时平均值和标准差
        dataifldsif(dataifldsif>0.3)=nan;
        datasfmsif(datasfmsif>0.3)=nan;
        dataifldsif=dataifldsif*10;
        datasfmsif=datasfmsif*10;
        dataifldmean=nanmean(dataifldsif);
        datasfmmean=nanmean(datasfmsif);
        dataifldsd=nanstd(dataifldsif);
        datasfmsd=nanstd(datasfmsif);
        % 
        newdata=[newdata;datat,dataifldsif,datasfmsif];
        halfhour=[halfhour;[t2,dataifldmean,datasfmmean,dataifldsd,datasfmsd]];
    end
end

xlswrite('D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\SIF_QE_allclean.xlsx',{'time','iFLD','SFM'},1,'A1');
xlswrite('D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\SIF_QE_allclean.xlsx',newdata,1,'A2');
xlswrite('D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\SIF_QE_halfhour.xlsx',{'doy','iFLDmean','SFMmean','iFLDsd','SFMsd'},1,'A1');
xlswrite('D:\Data\shangqiu data\shang\Results_QEradiance_nocontrol\SIF_QE_halfhour.xlsx',halfhour,1,'A2');
