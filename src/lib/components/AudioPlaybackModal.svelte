<script lang="ts">
	import type { AudioEntry } from '../player/types.js'
	import type { Category } from '../category-themes.js'
	import CollapsibleText from "./CollapsibleText.svelte"
	import { getAudioDescription } from "../utils/spsq-parser.js"
	import { getCategoryTheme } from '../category-themes.js'

	let { show = false, audio = null, onclose = null }: { show: boolean, audio: (AudioEntry & { artwork: string }) | null, onclose: (() => void) | null } = $props()

	let description = $state<string[]>([])
	let loading = $state(false)
	let categoryTheme = $derived(audio ? getCategoryTheme(audio.category as Category) : null)

	$effect(() => {
		if (show && audio?.path) {
			loading = true
			getAudioDescription(audio.path)
				.then((lines) => {
					description = lines
					loading = false
				})
				.catch((err) => {
					console.error('Error fetching description:', err)
					description = []
					loading = false
				})
		} else {
			description = []
		}
	})

	function handleClose() {
		show = false
		if (onclose) onclose()
	}

	function handlePlay() {
		show = false
		if (onclose) onclose()
	}

	function handleOverlayClick(e: MouseEvent) {
		if (e.target === e.currentTarget) handleClose()
	}

	function handleOverlayKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') handleClose()
	}

	function getCategoryBorderColor(): string {
		if (!categoryTheme) return 'var(--line-strong)'

		const borderMatch = categoryTheme.borderClass.match(/border-(\w+)-500\/(\d+)/)
		if (!borderMatch) return 'var(--line-strong)'

		const colorMap: Record<string, string> = {
			'rose': '244, 63, 94',
			'teal': '20, 184, 166',
			'amber': '245, 158, 11',
			'neutral': '115, 115, 115'
		}

		const color = colorMap[borderMatch[1]]
		const opacity = parseInt(borderMatch[2]) / 100

		if (color) {
			return `rgba(${color}, ${opacity})`
		}

		return 'var(--line-strong)'
	}

	function getCategoryBgColor(): string {
		if (!categoryTheme) return 'rgba(255, 250, 241, 0.98)'

		const bgMatch = categoryTheme.bgSubtleClass.match(/bg-(\w+)-500\/(\d+)/)
		if (!bgMatch) return 'rgba(255, 250, 241, 0.98)'

		const colorMap: Record<string, string> = {
			'rose': '244, 63, 94',
			'teal': '20, 184, 166',
			'amber': '245, 158, 11',
			'neutral': '115, 115, 115'
		}

		const color = colorMap[bgMatch[1]]
		const opacity = parseInt(bgMatch[2]) / 100

		if (color) {
			return `rgba(${color}, ${opacity})`
		}

		return 'rgba(255, 250, 241, 0.98)'
	}
</script>

{#if show && audio}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-[rgba(0,0,0,0.5)]" role="dialog" aria-modal="true" tabindex="-1" onclick={handleOverlayClick} onkeydown={handleOverlayKeydown}>
		<div
			class="relative rounded-2xl max-w-md w-full mx-4 p-6 pt-16 max-h-[90vh] overflow-y-auto border-2"
			style="background: var(--panel-strong); box-shadow: var(--shadow); border-color: {getCategoryBorderColor()};"
		>
			<button
				class="absolute top-4 left-4 hover:opacity-80 cursor-pointer"
				style="color: var(--muted);"
				onclick={handleClose}
				aria-label="Close modal"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>

			<div
				class="absolute inset-0 rounded-2xl pointer-events-none"
				style="background: {getCategoryBgColor()};"
			></div>

			<div class="relative z-10">
				<div class="flex flex-col items-center">
					{#if audio.artwork}
						<img
							src={audio.artwork}
							alt="Audio artwork"
							class="w-48 h-48 rounded-lg object-cover mb-4"
						/>
					{/if}

					{#if audio.author}
						<p class="text-sm mb-3" style="color: var(--muted);">created by {audio.author}</p>
					{/if}

					{#if loading}
						<p class="text-sm" style="color: var(--muted);">Loading description...</p>
					{:else if description.length > 0}
						<div class="w-full rounded-lg p-4 mb-6" style="background: var(--panel);">
							<CollapsibleText text={description.join("\n")} />
						</div>
					{/if}
				</div>

				<div class="flex gap-3">
					<button
						class="flex-1 py-3 px-4 rounded-lg cursor-pointer"
						style="background: var(--panel); color: var(--text); border: 1px solid var(--line);"
						onmouseenter={(e) => e.currentTarget.style.background = 'var(--panel-strong)'}
						onmouseleave={(e) => e.currentTarget.style.background = 'var(--panel)'}
						onclick={handleClose}
					>
						Cancel
					</button>
					<button
						class="flex-1 py-3 px-4 rounded-lg font-semibold cursor-pointer"
						style="background: var(--accent); color: white;"
						onmouseenter={(e) => e.currentTarget.style.background = 'var(--accent-strong)'}
						onmouseleave={(e) => e.currentTarget.style.background = 'var(--accent)'}
						onclick={handlePlay}
					>
						PLAY!
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
