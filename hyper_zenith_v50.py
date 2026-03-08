
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, Descriptors3D
import math

def de_novo_generative_score(mol):
    """Measures how 'hallucinated' or exotic the molecule is."""
    # Based on rare atom-pair combinations
    num_heavy = mol.GetNumHeavyAtoms()
    if num_heavy == 0: return 0
    # Penalty for too many rare heteroatoms
    rare = len(mol.GetSubstructMatches(Chem.MolFromSmarts("[P,I,B,As,Se]")))
    complexity = rdMolDescriptors.CalcNumRings(mol) * 2 + Descriptors.MolWt(mol) / 100
    score = 100 - (rare * 15 + complexity * 2)
    return round(max(0, min(100, score)), 1)

def geometric_shape_descriptors(mol):
    """3D-aware shape metrics (Heuristic approximations without full 3D optimization)."""
    # Using 2D proxies for 3D shape
    # Eccentricity (0 = circular, 1 = linear)
    # Globularity (1 = sphere)
    fsp3 = Descriptors.FractionCSP3(mol)
    rot = rdMolDescriptors.CalcNumRotatableBonds(mol)
    rings = rdMolDescriptors.CalcNumRings(mol)
    
    # Heuristic Globularity: lots of sp3 + rings = sphere-like
    glob = (fsp3 * 0.5 + (rings/(rings+1)) * 0.5) if rings > 0 else fsp3 * 0.3
    ecc = 1 - glob
    return {
        "Globularity_Est": round(glob, 2),
        "Eccentricity_Est": round(ecc, 2)
    }

def crystal_lattice_energy_hint(mw, lp, tp):
    """Heuristic for lattice stability (kJ/mol)."""
    # High MW, High TPSA, and Rigid structures have high lattice energy
    energy = (mw * 0.1) + (tp * 0.5) - (lp * 2)
    return round(energy, 1)

def metabolic_oxidative_exposure(mol):
    """Predicts density of CYP-mediated oxidative sites."""
    # Count of unhindered CH, CH2, CH3 and aromatic C-H
    ch = len(mol.GetSubstructMatches(Chem.MolFromSmarts("[CX4H3,CX4H2,CX4H1]")))
    arom_ch = len(mol.GetSubstructMatches(Chem.MolFromSmarts("[cX3H1]")))
    total = ch + arom_ch
    heavy = mol.GetNumHeavyAtoms()
    return round(total / heavy, 2) if heavy > 0 else 0

def brain_blood_ratio_logbb(lp, tp):
    """Refined LogBB (Wager equation)."""
    # LogBB = 0.33*logP - 0.015*TPSA + 0.4
    return round(0.33 * lp - 0.015 * tp + 0.4, 2)

def plasma_protein_binding_heuristic(lp):
    """Probability of >90% binding."""
    if lp > 4.5: return "Very High ( > 95%)"
    if lp > 3.0: return "High ( 80-95%)"
    return "Moderate/Low"

def aqueous_solubility_cat(lp, mw):
    """Categorical solubility at pH 7.4."""
    if lp < 1: return "Highly Soluble"
    if lp < 3: return "Modest Solubility"
    if lp > 5: return "Poor (Hydrophobic)"
    return "Standard"

def lead_optimization_direction(r):
    """Deep-Sense recommendation for next SAR steps."""
    if r['LogP'] > 5: return "Reduce Lipophilicity (Add Polar Groups)"
    if r['MW'] > 500: return "Truncate Structure (MW Reduction)"
    if r['TPSA'] < 20: return "Increase Polar Surface Area"
    return "Balanced Optimization"

def get_hzenith_v100(mol, res):
    mw = Descriptors.MolWt(mol); lp = Descriptors.MolLogP(mol); tp = Descriptors.TPSA(mol)
    
    data = {
        "DeNovo_Score": de_novo_generative_score(mol),
        "Lattice_Energy": crystal_lattice_energy_hint(mw, lp, tp),
        "Oxidative_Exposure": metabolic_oxidative_exposure(mol),
        "LogBB_Wager": brain_blood_ratio_logbb(lp, tp),
        "PPB_Estimate": plasma_protein_binding_heuristic(lp),
        "pH_7_4_Solubility": aqueous_solubility_cat(lp, mw),
        "Lead_SAR_Hint": lead_optimization_direction(res),
        "Kinase_Likeness": kinase_likeness(mol),
        "GPCR_Antag": gpcr_antagonist_profile(mol),
        "REACH_Status": reach_compliance_alert(mol),
        "Ion_Channel_Risk": ion_channel_blockade(mol),
        "PROTAC_Score": protac_potential(mol),
        "XAI_Reasoning": xai_explain_fail(res)
    }
    data.update(geometric_shape_descriptors(mol))
    return data
