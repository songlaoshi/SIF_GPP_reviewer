clear all;
clc;

fluxpath='D:\Data\shangqiu data\flux data';

[fluxdata,text]=xlsread([fluxpath '\SQ_EC_20171105.xlsx']);
Date=[];
for i=2:size(text,1)
    datestr=text{i,1};
    [y,mon,d,h,m,s]=datevec(datestr,'yyyy/mm/dd');
    monstr=num2str(mon);
    dstr=num2str(d);
    if mon/10<1
        monstr=['0' num2str(mon)];
    end
    if d/10<1
        dstr=['0' num2str(d)];
    end
    datestr=[num2str(y) monstr dstr];
    Date=[Date;{datestr}];
end

hour=fluxdata(:,1);
ta=fluxdata(:,13);
press=fluxdata(:,51)/100; % Pa to hPa


xlswrite('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab_code\atmos_correction\Tem_press_all_data.xlsx',Date,1,'A1');
xlswrite('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab_code\atmos_correction\Tem_press_all_data.xlsx',hour,1,'B1');
xlswrite('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab_code\atmos_correction\Tem_press_all_data.xlsx',ta,1,'C1');
xlswrite('D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\matlab_code\atmos_correction\Tem_press_all_data.xlsx',press,1,'D1');