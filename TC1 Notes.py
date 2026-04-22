#TC1 notes

def consider_adding_motivation(
        self,
        mtype,
        urgency=1,
        target=None,
        source=None,
        status_type=None,
    ):
        npc = self.owner#edited

        # --- TERMINAL / CONDITIONAL SUPPRESSION ---
        if mtype == "obtain_ranged_weapon":#Being a general use class, this TC1/GangMember was removed 
            if npc.inventory.has_ranged_weapon():
                # mark as suppressed, not forgotten
                self.suppressed[mtype] = {
                    "reason": "already_armed",
                    "until": "inventory_change",
                }
                debug_print(
                    npc,
                    f"[MOTIVE] Suppressed {mtype} (already armed)",
                    category="motive",
                )
                return False
            existing = self.get_motivation(mtype)
            if existing:
                old = existing.urgency
                existing.urgency = max(existing.urgency, float(urgency))
                debug_print(
                    npc,
                    f"[MOTIVE] Updated {mtype} urgency {old} → {existing.urgency} (source={source})",
                    category="motive",
                )
                return existing

            motive = self._create_motivation(mtype, urgency, target, source, status_type)
            debug_print(
                npc,
                f"[MOTIVE] Added {mtype} (urgency={urgency}, source={source})",
                category="motive",
            )
            return motive


        # --- CLEAR SUPPRESSION IF CONDITION NO LONGER HOLDS ---
        if mtype in self.suppressed:
            del self.suppressed[mtype]#what is this doing? Will it run automatically

        # --- PASS THROUGH TO REAL ADD/UPDATE ---
        self.update_motivations(
            motivation_type=mtype,
            urgency=urgency,
            target=target,
            source=source,
            status_type=status_type,
        )
        return True