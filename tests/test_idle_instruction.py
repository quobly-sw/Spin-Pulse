# --------------------------------------------------------------------------------------
# This code is part of SpinPulse.
#
# (C) Copyright Quobly 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
# --------------------------------------------------------------------------------------
""""""

from unittest.mock import MagicMock, patch

import matplotlib.pyplot as plt
import numpy as np

import tests.fixtures.dummy_objects as dm
from spin_pulse.instructions import IdleInstruction

# --------------------------------------------------------------------
# TESTS
# --------------------------------------------------------------------


def test_init_sets_name_and_duration_and_qubits():
    """Couvre __init__ et la structure de base de l'objet."""
    q = dm.DummyQubit(idx=3)
    idle = IdleInstruction([q], duration=7)

    # duration, name, qubits
    assert idle.duration == 7
    assert idle.name == "delay"
    assert idle.qubits[0] is q
    assert idle.qubits[0]._index == 3

    # str() doit inclure "IdlePulse" et la durée
    as_text = str(idle)
    assert "IdlePulse" in as_text
    assert "duration=7" in as_text
    assert as_text.strip().startswith("IdlePulse")


def test_adjust_duration_mutates_duration_in_place():
    """Couvre adjust_duration(), vérifie mutation."""
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=5)
    idle.adjust_duration(11)
    assert idle.duration == 11
    # re-change to ensure it's not write-once
    idle.adjust_duration(1)
    assert idle.duration == 1


def test_plot_calls_matplotlib_with_expected_line_segments():
    """
    Couvre plot():
    - si ax fourni
    - t_start != 0
    - duration arbitraire
    Vérifie que la ligne tracée correspond [t_start, t_start+duration-1], [0,0].
    """
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=4)

    fig, ax = plt.subplots()
    with patch.object(ax, "plot") as mock_plot:
        idle.plot(ax=ax, t_start=10, label_gates=False)

        mock_plot.assert_called_once()
        x_arg, y_arg = mock_plot.call_args[0]

        # On s'attend à un segment horizontal, de t_start à t_start+duration-1
        assert x_arg == [10, 10 + 4 - 1]
        assert y_arg == [0, 0]

        # Optionnel: vérifier qu'une 'color' a été passée
        assert "color" in mock_plot.call_args.kwargs
        assert mock_plot.call_args.kwargs["color"] == "k"

    plt.close(fig)


def test_plot_without_ax_uses_gca():
    """
    Couvre le chemin où ax=None -> utilise plt.gca().
    On mock plt.gca() pour contrôler l'axe retourné.
    """
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=3)

    fake_ax = MagicMock()
    with (
        patch("spin_pulse.instructions.idle.plt.gca", return_value=fake_ax),
        patch.object(fake_ax, "plot") as mock_plot,
    ):
        idle.plot(ax=None, t_start=2, label_gates=True)

        # Le plot doit avoir été appelé sur fake_ax
        mock_plot.assert_called_once()
        x_arg, y_arg = mock_plot.call_args[0]
        assert x_arg == [2, 2 + 3 - 1]
        assert y_arg == [0, 0]


def test_to_hamiltonian_returns_zero_hamiltonian_and_zero_times():
    """
    Couvre to_hamiltonian():
    - Vérifie la forme du Hamiltonien (2**num_qubits x 2**num_qubits)
    - Vérifie que tout est bien zéro
    - Vérifie la longueur du vecteur temps
    """
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=5)

    H, t = idle.to_hamiltonian()

    # 1 seul qubit -> matrice 2x2
    assert isinstance(H, np.ndarray)
    assert H.shape == (2, 2)
    assert np.allclose(H, 0.0)

    # t est un array style range(self.duration) * 0 -> donc 0s
    assert isinstance(t, np.ndarray)
    assert t.shape == (idle.duration,)
    assert np.allclose(t, 0.0)

    # petit contrôle cohérent: pas de NAN
    assert not np.isnan(H).any()
    assert not np.isnan(t).any()


# --------------------------------------------------------------------
# to_dynamical_decoupling()
# --------------------------------------------------------------------


def test_dd_mode_none_returns_self_only():
    """
    Branche mode=None :
    - Retourne simplement [self]
    - Ne touche pas à hardware_specs.rotation_generator
    """
    hw = dm.DummyHardwareSpecs(rot_duration=2)
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=10)

    seq = idle.to_dynamical_decoupling(hw, mode=None)
    assert isinstance(seq, list)
    assert len(seq) == 1
    assert seq[0] is idle

    # Aucune rotation demandée
    assert hw.rotation_generator.calls == []


def test_dd_mode_spin_echo_enough_time_happy_path():
    """
    Branche mode='spin_echo' quand la durée est suffisante.
    On attend :
      [IdleInstruction, X_instruction_1, IdleInstruction, X_instruction_2]
    Où:
      - X_instruction_* viennent de rotation_generator.from_angle("x", [qubit], pi)
      - idle_instruction_* ont une durée calculée par:
            duration_idle = int((self.duration - 2*X_duration)//2)
        et doivent être >= 0
    On vérifie :
      - la longueur de la séquence
      - le type/ordre
      - les durées calculées
      - que les pulses X utilisent le *même* qubit
    """
    hw = dm.DummyHardwareSpecs(rot_duration=3)  # chaque X_instruction a duration=3
    q = dm.DummyQubit(idx=7)
    idle = IdleInstruction([q], duration=20)

    seq = idle.to_dynamical_decoupling(hw, mode="spin_echo")

    # Doit donner 4 éléments
    assert len(seq) == 4

    idle1, x1, idle2, x2 = seq

    # idle1 et idle2 doivent être IdleInstruction
    assert isinstance(idle1, IdleInstruction)
    assert isinstance(idle2, IdleInstruction)

    # x1 et x2 sont des mocks créés par  dm.DummyRotationGenerator
    assert hasattr(x1, "axis") and x1.axis == "x"
    assert hasattr(x2, "axis") and x2.axis == "x"
    assert np.isclose(x1.angle, np.pi)
    assert np.isclose(x2.angle, np.pi)

    # Les qubits utilisés dans les X doivent être celui d'origine
    assert x1.qubits[0] is q
    assert x2.qubits[0] is q

    # Calcul attendu des durées idle :
    # X_duration = 3, total self.duration=20
    # duration_idle = int((20 - 2*3)//2) = int((20-6)//2)=int(14//2)=7
    assert idle1.duration == 7
    assert idle2.duration == 7

    # Assure qu'on a bien fait 2 appels à rotation_generator
    assert len(hw.rotation_generator.calls) == 2
    for axis, angle, qubits in hw.rotation_generator.calls:
        assert axis == "x"
        assert np.isclose(angle, np.pi)
        assert qubits == (q,)


def test_dd_mode_spin_echo_not_enough_time_returns_self():
    """
    Branche mode='spin_echo' mais durée trop courte:
    si duration_idle < 0 => retourne [self] seulement.
    Condition:
        duration_idle = int((self.duration - 2*X_duration)//2)
    Si cela devient négatif, alors aucun découpage.
    """
    # Choisissons rot_duration gros pour rendre duration_idle < 0
    hw = dm.DummyHardwareSpecs(rot_duration=10)  # X_duration = 10
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=15)

    seq = idle.to_dynamical_decoupling(hw, mode="spin_echo")

    # Ici:
    # duration_idle = int((15 - 2*10)//2) = int((-5)//2) = -3 (négatif)
    # => devrait retourner [self]
    assert len(seq) == 1
    assert seq[0] is idle

    # On a quand même appelé rotation_generator.from_angle deux fois
    # (X_instruction_1 et X_instruction_2 sont créés avant calcul)
    assert len(hw.rotation_generator.calls) == 2


def test_dd_mode_full_drive_with_positive_loops():
    """
    Branche mode='full_drive' avec n_loops > 0.
    Code:
        twopi_instruction = from_angle("x", [q], 2*pi)
        n_loops = self.duration // twopi_instruction.duration
        if n_loops > 0:
            npi_instruction = from_angle("x", [q], 2*pi*n_loops)
            npi_instruction.adjust_duration(self.duration)
            return [npi_instruction]
    On vérifie:
      - la liste fait 1 élément
      - l'angle correspond à 2*pi*n_loops
      - la durée de l'instruction finale == self.duration
    """
    hw = dm.DummyHardwareSpecs(rot_duration=4)
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=10)

    seq = idle.to_dynamical_decoupling(hw, mode="full_drive")
    assert len(seq) == 1
    instr = seq[0]

    # On a appelé from_angle au moins deux fois:
    # - une pour "twopi_instruction"
    # - une pour "npi_instruction"
    assert len(hw.rotation_generator.calls) >= 2

    # Calculons ce qu'on attend:
    # twopi_instruction.duration = 4
    # n_loops = 10 // 4 = 2
    # angle final attendu: 2*pi * n_loops = 4*pi
    expected_n_loops = idle.duration // hw.rotation_generator.base_duration
    expected_angle = 2 * np.pi * expected_n_loops

    assert np.isclose(instr.angle, expected_angle)
    assert instr.duration == idle.duration  # doit avoir été ajusté
    assert instr.qubits[0] is q
    assert instr.axis == "x"


def test_dd_mode_full_drive_zero_loops_returns_self():
    """
    Branche mode='full_drive' avec n_loops == 0.
    Cela arrive si self.duration < twopi_instruction.duration.
    Dans ce cas, to_dynamical_decoupling() retourne [self].
    """
    hw = dm.DummyHardwareSpecs(rot_duration=20)  # twopi duration = 20
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=5)  # 5 // 20 = 0 loops

    seq = idle.to_dynamical_decoupling(hw, mode="full_drive")
    assert len(seq) == 1
    assert seq[0] is idle

    # On aura quand même fait au moins 1 appel à rotation_generator.from_angle
    # (pour twopi_instruction)
    assert len(hw.rotation_generator.calls) >= 1


def test_dd_mode_unknown_is_treated_like_none():
    """
    Cette classe ne définit pas explicitement de 'else' pour des modes inconnus,
    mais si quelqu'un appelle mode="foobar", d'après le code actuel,
    ce n'est pris ni par spin_echo ni full_drive -> on tombe dans le dernier 'elif' ? Non.
    Il n'y a pas de 'else:' final. Donc actuellement, mode inconnu => pas de return explicite.
    En Python, ça renverrait None.
    On va vérifier ce comportement pour documenter son effet réel.
    (C'est important pour la couverture et pour capturer l'intention.)
    """
    hw = dm.DummyHardwareSpecs()
    q = dm.DummyQubit()
    idle = IdleInstruction([q], duration=10)

    result = idle.to_dynamical_decoupling(hw, mode="totally_weird_mode")
    # Selon l'implémentation fournie, il n'y a pas de `else:` final.
    # Donc la fonction tombe en bas sans `return`, donc `None`.
    assert result is None
