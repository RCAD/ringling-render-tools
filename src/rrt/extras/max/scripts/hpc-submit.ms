--macroScript HPC_UI
	--category:"DragAndDrop"
	--toolTip:"HPC Rendering Tools"
(
	global uuid
	fn GenerateIniName = (
		date = getLocalTime()
		uuid = (date[1] as string)+(date[2] as string)+(date[4] as string)+
		(date[5] as string)+(date[6] as string)+(date[7] as string)
		
		maxFile = getfilenamefile maxfilename
		
		filename = uuid+"_"+maxFile+".ini"
	)
	
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
		ini = "renderer = max\n"+
				"name = "+fld_title.text+"\n"+
				"project = "+unc_in+sysinfo.username+"\\max\\remote\n"+
				"output = "+unc_out+sysinfo.username+"\\"+uuid+"\\"+fld_title.text+".jpg\n"+
				"scene = "+unc_in+sysinfo.username+"\\max\\remote\\"+maxfilename as string+"\n"+
				"logs = "+unc_log+sysinfo.username+"\\"+uuid+"\\"+fld_title.text+".*.txt\n"+
				"start = "+fld_start.text+"\n"+
				"end = "+fld_end.text+"\n"
		format "%" ini to:fstream
		close fstream		
		fullpath = fullpath
	)
	
	rollout HPC "Send to HPC Cluster" width:327 height:245
	(
		GroupBox grb_main "HPC Submission Tool" pos:[2,3] width:323 height:196
		GroupBox grb_sub "" pos:[3,198] width:319 height:39
		label lbl_title "Title:" pos:[56,38] width:24 height:16
		label lbl_start "Start Frame:" pos:[17,61] width:63 height:15
		label lbl_end "End Frame:" pos:[23,87] width:57 height:17
		label lbl_step "Frame Step:" pos:[20,113] width:60 height:16
		edittext fld_title "" pos:[82,37] width:229 height:17
		edittext fld_start "" pos:[82,63] width:229 height:17
		edittext fld_end "" pos:[82,88] width:229 height:17
		edittext fld_step "" pos:[82,113] width:229 height:17
		button btn_submit "SUBMIT" pos:[20,209] width:287 height:22
			
		on btn_submit pressed do
		(
			--GENERATE INI FILE
			filePath = GenerateIniFile fld_title fld_start fld_end
			-- LAUNCH COMMAND
			DOSCommand ("echo "+filePath+" & pause")
			
		)
	)
	HPC_Floater = newrolloutfloater "HPC Submit" 355 275
	addrollout HPC HPC_Floater
	
	
)