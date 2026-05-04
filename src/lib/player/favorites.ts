import { writable } from 'svelte/store';

const storageKey = 'synapseq-hub:favorites';

function loadFavorites(): string[] {
	try {
		const raw = localStorage.getItem(storageKey);
		if (raw === null) return [];
		const parsed = JSON.parse(raw) as unknown;
		if (!Array.isArray(parsed)) return [];
		return parsed.filter((item): item is string => typeof item === 'string');
	} catch {
		return [];
	}
}

function writeFavorites(ids: string[]): void {
	try {
		localStorage.setItem(storageKey, JSON.stringify(ids));
	} catch {
		// Local persistence is optional; the in-memory player still works.
	}
}

export const favoritesStore = writable<string[]>(loadFavorites());

export function addFavorite(id: string): void {
	favoritesStore.update((current) => {
		if (current.includes(id)) return current;
		const next = [...current, id];
		writeFavorites(next);
		return next;
	});
}

export function removeFavorite(id: string): void {
	favoritesStore.update((current) => {
		const next = current.filter((favId) => favId !== id);
		writeFavorites(next);
		return next;
	});
}

export function getFavorites(): string[] {
	let result: string[] = [];
	favoritesStore.subscribe((ids) => { result = ids; })();
	return result;
}

export function clearFavorites(): void {
	favoritesStore.set([]);
	writeFavorites([]);
}
