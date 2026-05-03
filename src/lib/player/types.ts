export type Theme = 'light' | 'dark';

export type AudioEntry = {
	id: string;
	name: string;
	author: string;
	path: string;
	category: string;
	download_url: string;
	updated_at: string;
	dependencies: string[];
};

export type Manifest = {
	version: string;
	lastUpdated: string;
	entries: AudioEntry[];
};
