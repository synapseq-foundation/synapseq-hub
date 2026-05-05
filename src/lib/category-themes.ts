export type Category = 'All' | 'Favorites' | 'Focus' | 'Meditation' | 'Relaxation' | 'Sleep';

export type CategoryTheme = {
	bgClass: string;
	bgSubtleClass: string;
	borderClass: string;
	headerBorderClass: string;
	headerBgGradientClass: string;
	transitionClass: string;
};

export const categoryThemes: Record<Exclude<Category, 'All'>, CategoryTheme> = {
	Favorites: {
		bgClass: 'bg-rose-500/30',
		bgSubtleClass: 'bg-rose-500/10',
		borderClass: 'border-rose-500/60',
		headerBorderClass: 'border-rose-500/60',
		headerBgGradientClass: 'bg-gradient-to-r from-rose-500/5 via-transparent to-rose-500/5',
		transitionClass: 'transition-colors duration-300 ease-in-out'
	},
	Focus: {
		bgClass: 'bg-teal-500/30',
		bgSubtleClass: 'bg-teal-500/10',
		borderClass: 'border-teal-500/60',
		headerBorderClass: 'border-teal-500/60',
		headerBgGradientClass: 'bg-gradient-to-r from-teal-500/5 via-transparent to-teal-500/5',
		transitionClass: 'transition-colors duration-300 ease-in-out'
	},
	Relaxation: {
		bgClass: 'bg-amber-500/30',
		bgSubtleClass: 'bg-amber-500/10',
		borderClass: 'border-amber-500/60',
		headerBorderClass: 'border-amber-500/60',
		headerBgGradientClass: 'bg-gradient-to-r from-amber-500/5 via-transparent to-amber-500/5',
		transitionClass: 'transition-colors duration-300 ease-in-out'
	},
	Meditation: {
		bgClass: 'bg-neutral-500/30',
		bgSubtleClass: 'bg-neutral-500/10',
		borderClass: 'border-neutral-500/60',
		headerBorderClass: 'border-neutral-500/60',
		headerBgGradientClass: 'bg-gradient-to-r from-neutral-500/5 via-transparent to-neutral-500/5',
		transitionClass: 'transition-colors duration-300 ease-in-out'
	},
	Sleep: {
		bgClass: 'bg-indigo-400/30',
		bgSubtleClass: 'bg-indigo-400/10',
		borderClass: 'border-indigo-400/50',
		headerBorderClass: 'border-indigo-400/50',
		headerBgGradientClass: 'bg-gradient-to-r from-indigo-400/5 via-transparent to-indigo-400/5',
		transitionClass: 'transition-colors duration-300 ease-in-out'
	}
};

export function getCategoryTheme(category: Category): CategoryTheme | null {
	if (category === 'All') return null;
	return categoryThemes[category] ?? null;
}
