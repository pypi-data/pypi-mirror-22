# getCDFs
This will check for cdfs on your computer. If they don't exist, or there's an updated version on the server, it will download from the server. It will then load the cdfs using spacepy.pycdf, and place them into a dictionary.

##Usage:
getCDFs(getCDFs(datetime, string, string, **kw):

    date: Python datetime object containing the date that you want cdfs for.
    craft: character - 'A' or 'B'.
    species: character - 'H', 'He', or 'O'.
    RBlevel: string - RBSPICE data level; '3PAP', '3', '2', '1', or '0'
    Hlevel: string - HOPE data level; '3', or '2'
    Hproduct: string - If using, HOPE level 3 data, which product; 'PA' or 'MOM'
	Maglevel: string - MagEIS data level; '3', or '2'
    EMlevel: string - EMFISIS data level; '4', '3', or '2'
    PH: string describing which Time of Flight by Pulse Height product you want: 
    	'LEHT'(Low Energy, High Time resolution) or 'HELT'(High Energy, Low Time resolution).
    EMF: string describing which EMFISIS product you want: 
    	('1sec', '4sec', or 'hires')+'-'+('gei', 'geo', 'gse', 'gsm', or 'sm').
    check: When True, it will query the server for updated versions. 
    	If False, then the server will not be queried at all. 
    	If you don't have the file on your computer, it will not be downloaded. 
	Set this keyword to False if you do not have internet access.
    The last five keywords describe which data product you want.
    	All is default, but if you set any one or more of them to True, will override this.

    Returns: Python dictionary containing spacepy cdf objects. 
    Keys are 'TOFxE', 'TOFxPH', 'HOPE', 'MagEIS', and 'EMFISIS'
	
changeRoot()

	On the first run, you will be asked to set a root directory where your files will be stored.
	This function will allow you to change this.
