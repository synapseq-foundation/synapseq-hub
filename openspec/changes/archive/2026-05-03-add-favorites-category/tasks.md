## 1. Favorites Storage Utility

- [x] 1.1 Create a `src/lib/player/favorites.ts` module with functions to get, add, and remove favorite audio IDs from the `synapseq-hub:favorites` localStorage key
- [x] 1.2 Ensure the module initializes the favorites array as empty if the localStorage key does not exist
- [x] 1.3 Export a reactive Svelte store or function to allow components to subscribe to favorites changes

## 2. Update Favorite Toggle Logic

- [x] 2.1 Update the favorite toggle handler to use the new `favorites.ts` module instead of the old limit and list-top logic
- [x] 2.2 Remove the 5-item favorite limit check from the toggle handler
- [x] 2.3 Remove the logic that moves favorited items to the top of the audio list

## 3. Add Favorites Category Tab

- [x] 3.1 Add a "Favorites" tab to the category badges list, positioned immediately after "All"
- [x] 3.2 Update the category selection state to handle the "Favorites" tab as a special case
- [x] 3.3 Add "Favorites" to the category color mapping in `src/lib/category-themes.ts` (or handle it separately)

## 4. Favorites Category Rendering

- [x] 4.1 Update the audio list filtering logic to show only favorited audio entries when "Favorites" category is selected
- [x] 4.2 Implement the empty state message when the Favorites category is selected and no favorites exist
- [x] 4.3 Ensure unfavoriting an item while in the Favorites category immediately removes it from the list view

## 5. Cleanup and Verification

- [x] 5.1 Remove any remaining legacy favorite ordering and limit code
- [x] 5.2 Verify the "Favorites" tab appears correctly next to "All"
- [x] 5.3 Verify favoriting/unfavoriting works across all categories and persists after page reload
- [x] 5.4 Verify the Favorites category shows all favorited items and unfavoriting removes them immediately
