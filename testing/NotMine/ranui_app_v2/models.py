"""
models.py
OOP classes for the Ranui Family Clothing Allowance App.
"""

ANNUAL_ALLOWANCE = 300.00
BONUS_THRESHOLD  = 50.00


class Child:
    """Represents a child in the Ranui family."""

    def __init__(self, name: str, balance: float = ANNUAL_ALLOWANCE):
        self._name    = name
        self._balance = balance

    # ── Getters ──────────────────────────────────────────
    @property
    def name(self) -> str:
        return self._name

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def on_target_for_bonus(self) -> bool:
        """True if still possible to finish year with >$50 remaining."""
        return self._balance > BONUS_THRESHOLD

    @property
    def bonus_status(self) -> str:
        return "✅ On target for bonus" if self.on_target_for_bonus else "❌ No bonus"

    # ── Methods ──────────────────────────────────────────
    def spend(self, amount: float) -> bool:
        """Deduct amount. Returns True on success, False if insufficient funds."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def reset(self):
        self._balance = ANNUAL_ALLOWANCE

    def __repr__(self):
        return f"Child(name={self._name!r}, balance={self._balance:.2f})"


class Family:
    """Represents the Ranui family — a collection of Child objects."""

    def __init__(self, name: str):
        self._name     = name
        self._children: list[Child] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def children(self) -> list[Child]:
        return self._children

    def add_child(self, child: Child):
        self._children.append(child)

    def get_child(self, name: str) -> Child | None:
        for child in self._children:
            if child.name == name:
                return child
        return None

    def bonus_eligible(self) -> list[Child]:
        return [c for c in self._children if c.on_target_for_bonus]

    def reset_all(self):
        for child in self._children:
            child.reset()

    def __repr__(self):
        return f"Family(name={self._name!r}, children={self._children})"
