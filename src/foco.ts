import { nextTick } from 'vue'

// Leva o foco ao primeiro campo com erro, para quem usa teclado ou leitor de tela.
export async function focarPrimeiroErro(formulario: HTMLFormElement | null) {
  await nextTick()
  formulario?.querySelector<HTMLElement>('[aria-invalid="true"]')?.focus()
}
