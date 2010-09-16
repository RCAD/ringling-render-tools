--Creating the Ringling HPC menu
--THIS NEED TO BE IN THE .\plugins folder on max
 

if menuMan.registerMenuContext 0xe077b1d then (

-- Get the main menu bar
local mainMenuBar = menuMan.getMainMenuBar() 

-- Create a new menu
local subMenu = menuMan.createMenu "Ringling"
 
-- compute the index of the next-to-last menu item in the main menu bar
local subMenuIndex = mainMenuBar.numItems() - 1 

-- create a menu item that calls the sample macroScript
local HPCitem = menuMan.createActionItem "HPC" "Rendering" 

-- Add the item to the menu
subMenu.addItem HPCitem -1 

-- Create a new menu item with the menu as it's sub-menu
local subMenuItem = menuMan.createSubMenuItem "Ringling" subMenu 

-- Add the sub-menu just at the second to last slot
mainMenuBar.addItem subMenuItem subMenuIndex

-- redraw the menu bar with the new item
menuMan.updateMenuBar()

)
