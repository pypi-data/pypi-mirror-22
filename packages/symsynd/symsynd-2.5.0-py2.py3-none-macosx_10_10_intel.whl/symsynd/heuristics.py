from symsynd.utils import parse_addr


SIGILL = 4
SIGBUS = 10
SIGSEGV = 11


def get_previous_instruction(addr, cpu_name):
    if cpu_name.startswith('arm64'):
        return (addr & -4) - 4
    elif cpu_name.startswith('arm'):
        return (addr & -2) - 2
    else:
        return addr - 1


def get_next_instruction(addr, cpu_name):
    if cpu_name.startswith('arm64'):
        return (addr & -4) + 4
    elif cpu_name.startswith('arm'):
        return (addr & -2) + 2
    else:
        return addr + 1


def get_ip_register(registers, cpu_name):
    rv = None
    if registers:
        if cpu_name[:3] == 'arm':
            rv = registers.get('pc')
        elif cpu_name == 'x86_64':
            rv = registers.get('rip')
    if rv is not None:
        return parse_addr(rv)


def round_to_instruction_end(addr, cpu_name):
    if cpu_name.startswith('arm64'):
        return (addr & -4) + 3
    elif cpu_name.startswith('arm'):
        return (addr & -2) + 1
    return addr


def find_best_instruction(addr, cpu_name, meta=None):
    """Given an instruction and meta information this attempts to find
    the best instruction for the frame.  In some circumstances we can
    fix it up a bit to improve the accuracy.  For more information see
    `symbolize_frame`.
    """
    addr = rv = parse_addr(addr)

    # In case we're not on the crashing frame we apply a simple heuristic:
    # since we're most likely dealing with return addresses we just assume
    # that the call is one instruction behind the current one.
    if not meta or meta.get('frame_number') != 0:
        rv = get_previous_instruction(addr, cpu_name)

    # In case registers are available we can check if the PC register
    # does not match the given address we have from the first frame.
    # If that is the case and we got one of a few signals taht are likely
    # it seems that going with one instruction back is actually the
    # correct thing to do.
    else:
        regs = meta.get('registers')
        ip = get_ip_register(regs, cpu_name)
        if ip is not None and ip != addr and \
           meta.get('signal') in (SIGILL, SIGBUS, SIGSEGV):
            rv = get_previous_instruction(addr, cpu_name)

    # Don't ask me why we do this, but apparently on arm we get better
    # hits if we look at the end of an instruction in the DWARF file than
    # the beginning.
    return round_to_instruction_end(rv, cpu_name)
