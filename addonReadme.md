# NVDA Speech History

This is an updated version of the Clip Copy add-on for NVDA, initially created by Tyler Spivey in 2012.
The keystrokes were updated because the original keys could present conflicts with other applications, since very common keys were used in the original add-on, E.G. f12.

## features:

* A command to copy the most recent spoken text to the clipboard.
* Ability to review the 500 most recent items spoken by NVDA.
* Show a dialog with the current most recent items spoken by NVDA. You can review and copy the items.

## Usage.
	
	* review the most recent items spoken by NVDA: press NVDA + shift + f11 (previows item) or NVDA + shift + f12 (next item).
	* Copy the last item read by NVDA, or the current reviewed item: NVDA + shift + f12.
	* Show a dialog with the current most recent items spoken by NVDA: NVDA + alt + f12

### Speech history elements.

In this dialog, you will be focused in the most recent items spoken by NVDA, the most recent item first. You can navigate the items by using up and down arrow keys. Each element will show just 100 characters, but you can see the entire contend by pressing tab key in a multiline text edit field. Those items won't update with new items spoken by NVDA. If you want to update the list of items, you must restart this dialog.

You can search in the entire elements in the search edit field. Type some letters or words and then, press enter. The list of items will be updated according to your search. To clean the search, just clean the text in the search edit field, and press enter.

You can copy the current selected item, by using the copy button. Also, you can copy all current items with "Copy all" button. This will copy just the current items shown in the list, separated by a newline.

To close this dialog, press escape or close button.
