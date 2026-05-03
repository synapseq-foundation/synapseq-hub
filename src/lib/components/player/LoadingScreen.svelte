<script lang="ts">
  import { Headphones } from '@lucide/svelte';
</script>

<div class="fixed inset-0 z-[60] flex items-center justify-center bg-[var(--panel-strong)]/80 backdrop-blur-md">
  <div class="flex flex-col items-center gap-4">
    <Headphones class="h-12 w-12 text-[var(--muted)]" />
    <p class="text-sm text-[var(--muted)]">Loading audio catalog...</p>
  </div>
</div>
