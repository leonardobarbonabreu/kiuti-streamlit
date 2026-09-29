"""Formatação no padrão brasileiro."""

SITUACOES = {
    "na_meta": "Na meta",
    "abaixo_da_meta": "Abaixo da meta",
    "ficha_incompleta": "Ficha incompleta",
}


def reais(valor: float | None) -> str:
    """15.45 -> 'R$ 15,45'; 1234.5 -> 'R$ 1.234,50'; None -> '—' (ficha incompleta)."""
    if valor is None:
        return "—"
    texto = f"{valor:,.2f}"  # '1,234.50' (padrão americano)
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def numero(valor: float) -> str:
    """8.0 -> '8'; 0.5 -> '0,5'."""
    return f"{valor:g}".replace(".", ",")


if __name__ == "__main__":
    assert reais(15.45) == "R$ 15,45"
    assert reais(1234.5) == "R$ 1.234,50"
    assert reais(None) == "—"
    assert numero(8.0) == "8" and numero(0.5) == "0,5"
    print("ok")
