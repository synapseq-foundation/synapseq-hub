export type Category = 'All' | 'Focus' | 'Meditation' | 'Relaxation';

export type CategoryTheme = {
	bgClass: string;
	bgSubtleClass: string;
	borderClass: string;
	transitionClass: string;
};

export const categoryThemes: Record<Exclude<Category, 'All'>, CategoryTheme> = {
	Focus: {
		bgClass: 'bg-teal-500/30',
		bgSubtleClass: 'bg-teal-500/10',
		borderClass: 'border-teal-500/60',
		transitionClass: 'transition-colors duration-300 ease-in-out'
	},
	Relaxation: {
		bgClass: 'bg-amber-500/30',
		bgSubtleClass: 'bg-amber-500/10',
		borderClass: 'border-amber-500/60',
		transitionClass: 'transition-colors duration-300 ease-in-out'
	},
	Meditation: {
		bgClass: 'bg-neutral-500/30',
		bgSubtleClass: 'bg-neutral-500/10',
		borderClass: 'border-neutral-500/60',
		transitionClass: 'transition-colors duration-300 ease-in-out'
	}
};

export function getCategoryTheme(category: Category): CategoryTheme | null {
	if (category === 'All') return null;
	return categoryThemes[category] ?? null;
}
