
rollout TestRollout "Send to HPC"
(	
	edittext job_name "job title"
	edittext start "Start Frame" readonly:True text:(int(rendStart) as string)
	edittext end "End Frame" readonly:True text:(int(rendEnd) as string)
	edittext byFrame "Render Nth Frame" readonly:True text:(int(rendNthFrame) as string)
	button submit "Submit"
	
	
	fn updateValues
	(
		start.text = int(rendStart) as string
		end.text = int(rendEnd) as string
		byFrame.text = int(rendNthFrame) as string
	)
	callbacks.addScript(#renderParamsChanged, "updateValues()")
	
)
createDialog TestRollout