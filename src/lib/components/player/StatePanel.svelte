<script lang="ts">
	type Props = {
		message: string;
		role?: 'alert' | 'status';
	};

	let { message, role }: Props = $props();
</script>

<div class="m-[18px] rounded-3xl border border-[var(--line)] bg-[var(--panel-strong)] p-6 text-center text-[var(--muted)]" {role}>
	{message}
</div>
