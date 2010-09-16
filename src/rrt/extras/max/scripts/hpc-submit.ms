-- HPC submission tool for 3DS MAX

macroScript HPC
	category:"Rendering"
	toolTip:"HPC Rendering Tools"
(
	-- Initial global variable values set and render options pulled from Max 
	(
		global HPC_Floater
		global HPC_SPOOL_BIN = "C:\\Ringling\\HPC\\bin\\hpc-spool.bat"	
		global illegal_chars = "!\"#$%&\'()*+,:;<=>?@[]^`{|}~"
		global uuid = 0
		global def_title = getfilenamefile maxfilename as string
		global def_start = 1 as string
		global def_end = 1 as string
		global def_step = 1 as string
		
		case rendTimeType of  (
			1:(
				--single frame
				-- no changes to defaults
			)
			2:(
				--active time segment NOT SURE IF WE WILL ALLOW THIS
				def_start = animationRange.start as string
				def_start = substring def_start 1 (def_start.count-1)
				def_end = animationRange.end as string
				def_end = substring def_end 1 (def_end.count-1)
				def_step = rendNthFrame as string
			)
			3:(
				--Range
				def_start = rendStart as string
				def_start = substring def_start 1 (def_start.count-1)
				def_end = rendEnd as string
				def_end = substring def_end 1 (def_end.count-1)
				def_step = rendNthFrame as string
			)
			default:(
				--no change
			)
		)
	)
	
	-- Cleans the title of spaces and illegal characters
	fn cleanStr str = (
		--cleans spaces
		for i=1 to str.count do (
			if str[i]==" " then (
				str[i] = "_"
			)
		)
		
		-- cleans illegals
		token = filterstring str illegal_chars
		str = ""		
		for i=1 to token.count do (
			str += token[i]
		)
		
		if str.count < 1 then
			str = getfilenamefile maxfilename as string
		
		str = str
		
	)
	
	-- Generates the name of the ini file with the uuid and scene name
	fn GenerateIniName = (
		date = getLocalTime()
		uuid = (date[1] as string)+(date[2] as string)+(date[4] as string)+
		(date[5] as string)+(date[6] as string)+(date[7] as string)
		
		maxFile = getfilenamefile maxfilename
		
		filename = uuid+"_"+maxFile+".ini"
	)
	
	-- Generates ini file calling needed functions
	fn GenerateIniFile fld_title fld_start fld_end = (
		unc_in = "\\\chome\\chome\\"
		unc_out = "\\\chome\\coutput\\"
		unc_log = "\\\clogs\\clogs\\"
		uuid_path = "d:\\hpc\\"+sysinfo.username+"\\scripts\\"
		
		uuid_name = GenerateIniName()
		
		if not doesfileexist uuid_path then (
			makeDir uuid_path
		) 
		fullPath = uuid_path+uuid_name
		fstream = createFile fullPath
		title = cleanStr fld_title.text
		ini = "# Created for "+sysinfo.username+" on "+uuid+"\n"+
				"renderer = max\n"+
				"name = "+title+"\n"+
				"project = "+unc_in+sysinfo.username+"\\max\\remote\n"+
				"output = "+unc_out+sysinfo.username+"\\"+uuid+"\\"+title+".jpg\n"+
				"scene = "+unc_in+sysinfo.username+"\\max\\remote\\"+maxfilename as string+"\n"+
				"logs = "+unc_log+sysinfo.username+"\\"+uuid+"\\"+title+".*.txt\n"+
				"start = "+fld_start.text+"\n"+
				"end = "+fld_end.text+"\n"
		format "%" ini to:fstream
		close fstream
		fullpath = fullpath
	)
	
	-- Rollout Window
	rollout HPC "Send to HPC Cluster" width:327 height:245
	(
		
		GroupBox grb_main "HPC Submission Tool" pos:[2,3] width:283 height:146
		GroupBox grb_sub "" pos:[3,148] width:279 height:39
		label lbl_title "Title:" pos:[56,38] width:24 height:16
		label lbl_start "Start Frame:" pos:[17,61] width:63 height:15
		label lbl_end "End Frame:" pos:[23,87] width:57 height:17
		label lbl_step "Frame Step:" pos:[20,113] width:60 height:16
		edittext fld_title "" text:def_title pos:[82,37] width:189 height:17
		edittext fld_start "" text:def_start pos:[82,63] width:189 height:17 readOnly:true
		edittext fld_end "" text:def_end pos:[82,88] width:189 height:17 readOnly:true
		edittext fld_step "" text:def_step pos:[82,113] width:189 height:17 readOnly:true
		button btn_submit "SUBMIT" pos:[20,159] width:247 height:22		
			
		
		on btn_submit pressed do
		(
			
			--GENERATE INI FILE
			iniFilePath = GenerateIniFile fld_title fld_start fld_end
			-- LAUNCH COMMAND
			DOSCommand ("echo launchin "+HPC_SPOOL_BIN+" with ini "+iniFilePath+" & pause")
			closeRolloutFloater HPC_Floater
		)
	)
	HPC_Floater = newrolloutfloater "HPC Submit" 300 225
	addrollout HPC HPC_Floater
	
	
)