# NVDA Speech History

This is an updated version of the Clip Copy add-on for NVDA, initially created by Tyler Spivey in 2012.
The keystrokes were updated because the original keys could present conflicts with other applications, since very common keys were used in the original add-on, E.G, f12.

## features:

* A command to copy the most recent spoken text to the clipboard.
* Ability to review the 500 most recent items spoken by NVDA.
* Show a dialog with the current most recent items spoken by NVDA. You can review, multi-select items and copy the current item or items selected.

## Usage.
	
	* Review the most recent items spoken by NVDA: press NVDA + shift + f11 (previous item) or NVDA + shift + f12 (next item).
	* Copy the last item read by NVDA, or the current reviewed item: NVDA + control + f12.
	* Show a dialog with the current most recent items spoken by NVDA: NVDA + alt + f12

### Speech history elements.

In this dialog, you will be focused in the most recent items spoken by NVDA, the most recent item first. You can navigate the items by using up and down arrow keys. Each element will show just 100 characters, but you can see the entire contend by pressing tab key in a multiline text edit field. Those items won't update with new items spoken by NVDA. If you want to update the list of items, you must restart this dialog or press the "refresh history" button.

You can search in the entire elements in the search edit field. Type some letters or words and then, press enter. The list of items will be updated according to your search. To clean the search, just clean the text in the search edit field, and press enter. Also, a search will be made if you are in the search field, and the field loses the focus. E.G, by pressing tab or focus another control in some another way.

You can copy the current selected items, by using the copy button. This will copy all text shown in the field that contains all items selected.
Also, you can copy all current items with "Copy all" button. This will copy just the current items shown in the list, each one will be separated by a newline. If you searched something, then this button will only copy the items found.

If you want to select more than one item, use same keys as on windows. E.G, shift + up and down arrow keys to do contiguous selection, control + the same keys to do uncontiguous selection.
To close this dialog, press escape or close button.
