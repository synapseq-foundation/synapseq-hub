<script lang="ts">
	import type { AudioEntry } from '../player/types.js';
	import type { Category } from '../category-themes.js';
	import CollapsibleText from "./CollapsibleText.svelte";
	import { getAudioDescription } from "../utils/spsq-parser.js";
	import { getCategoryTheme } from '../category-themes.js';
	import { Check, X } from '@lucide/svelte';

	let {
		show = false,
		audio = null,
		onclose = null
	}: {
		show: boolean;
		audio: (AudioEntry & { artwork: string }) | null;
		onclose: (() => void) | null;
	} = $props();

	let description = $state<string[]>([]);
	let loading = $state(false);
	let categoryTheme = $derived(audio ? getCategoryTheme(audio.category as Category) : null);

	$effect(() => {
		if (show && audio?.path) {
			loading = true;
			getAudioDescription(audio.path)
				.then((lines) => {
					description = lines;
					loading = false;
				})
				.catch((err) => {
					console.error('Error fetching description:', err);
					description = [];
					loading = false;
				});
		} else {
			description = [];
		}
	});

	function handleClose() {
		if (onclose) onclose();
	}

	function handlePlay() {
		if (onclose) onclose();
	}

	function handleOverlayClick(e: MouseEvent) {
		if (e.target === e.currentTarget && onclose) onclose();
	}

	function handleOverlayKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') handleClose();
	}

	function getCategoryBorderColor(): string {
		if (!categoryTheme) return 'var(--line-strong)';

		const borderMatch = categoryTheme.borderClass.match(/border-(\w+)-500\/(\d+)/);
		if (!borderMatch) return 'var(--line-strong)';

		const colorMap: Record<string, string> = {
			rose: '244, 63, 94',
			teal: '20, 184, 166',
			amber: '245, 158, 11',
			neutral: '115, 115, 115'
		};

		const color = colorMap[borderMatch[1]];
		const opacity = parseInt(borderMatch[2]) / 100;

		if (color) {
			return `rgba(${color}, ${opacity})`;
		}

		return 'var(--line-strong)';
	}

	function getCategoryBgColor(): string {
		if (!categoryTheme) return 'rgba(255, 250, 241, 0.98)';

		const bgMatch = categoryTheme.bgSubtleClass.match(/bg-(\w+)-500\/(\d+)/);
		if (!bgMatch) return 'rgba(255, 250, 241, 0.98)';

		const colorMap: Record<string, string> = {
			rose: '244, 63, 94',
			teal: '20, 184, 166',
			amber: '245, 158, 11',
			neutral: '115, 115, 115'
		};

		const color = colorMap[bgMatch[1]];
		const opacity = parseInt(bgMatch[2]) / 100;

		if (color) {
			return `rgba(${color}, ${opacity})`;
		}

		return 'rgba(255, 250, 241, 0.98)';
	}
</script>

{#if show && audio}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-[rgba(0,0,0,0.5)]"
		role="dialog"
		aria-modal="true"
		tabindex="-1"
		onclick={handleOverlayClick}
		onkeydown={handleOverlayKeydown}
	>
		<div
			class="relative mx-4 max-h-[90vh] w-full max-w-md overflow-y-auto rounded-2xl border-2 p-6 pt-16"
			style="background: var(--panel-strong); box-shadow: var(--shadow); border-color: {getCategoryBorderColor()};"
		>
		<button
			class="absolute top-4 left-4 hover:opacity-80 cursor-pointer"
			style="color: var(--muted);"
			onclick={handleClose}
			aria-label="Close modal"
		>
			<X size={24} />
		</button>

			<div
				class="pointer-events-none absolute inset-0 rounded-2xl"
				style="background: {getCategoryBgColor()};"
			></div>

			<div class="relative z-10">
				<div class="flex flex-col items-center">
					{#if audio.artwork}
						<img
							src={audio.artwork}
							alt="Audio artwork"
							class="mb-4 h-48 w-48 rounded-lg object-cover"
						/>
					{/if}

					<!-- {#if audio.author}
						<p class="text-sm mb-3" style="color: var(--muted);">created by {audio.author}</p>
					{/if} -->

					{#if loading}
						<p class="text-sm" style="color: var(--muted);">Loading description...</p>
					{:else if description.length > 0}
						<div class="w-full rounded-lg p-4 mb-6" style="background: var(--panel); max-height: 350px; overflow-y: auto;">
							<CollapsibleText text={description.join("\n")} />
						</div>
					{/if}
				</div>

			<div class="flex gap-3">
				<button
					class="flex-1 py-3 px-4 rounded-lg cursor-pointer font-semibold inline-flex items-center justify-center gap-2"
					style="background: var(--accent); color: white;"
					onmouseenter={(e) => e.currentTarget.style.background = 'var(--accent-strong)'}
					onmouseleave={(e) => e.currentTarget.style.background = 'var(--accent)'}
					onclick={handleClose}
				>
					<Check size={18} />
					Ok
				</button>
			</div>
			</div>
		</div>
	</div>
{/if}
