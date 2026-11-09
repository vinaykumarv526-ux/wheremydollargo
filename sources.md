# WhereMyDollarGo: Primary Sources Registry & Fact Archive

Every statistic, calculation, and quote used in scripts must be referenced directly from an authoritative primary source before entering production.

---

## 1. Authoritative Institutional Sources

| Institution | Domain / Data Scope | Official Reference URL |
|---|---|---|
| **Bureau of Labor Statistics (BLS)** | Median wages, CPI inflation, consumer expenditure | https://www.bls.gov |
| **Internal Revenue Service (IRS)** | Federal tax brackets, standard deduction, 401(k)/IRA contribution caps | https://www.irs.gov |
| **Social Security Administration (SSA)** | OASDI wage caps, benefit formulas, COLA adjustments | https://www.ssa.gov |
| **Federal Reserve System (Fed)** | Federal funds rate, interest rate projections, H.15 releases | https://www.federalreserve.gov |
| **Federal Deposit Insurance Corp (FDIC)** | Deposit insurance limits ($250,000 per depositor/institution) | https://www.fdic.gov |
| **Consumer Financial Protection Bureau (CFPB)** | Credit report regulations, APR rules, mortgage disclosure | https://www.consumerfinance.gov |
| **National Association of Insurance Commissioners (NAIC)** | State insurance regulations, loss ratios, complaint indices | https://content.naic.org |
| **Centers for Medicare & Medicaid Services (CMS)** | Medical Loss Ratio (80/20 rule), ACA benchmark rules | https://www.cms.gov |
| **Energy Information Administration (EIA)** | Gasoline price breakdowns (crude, refining, distribution, taxes) | https://www.eia.gov/petroleum/gasdiesel/ |

---

## 2. Verified Benchmark Data Reference Points (Current Tax Year Baseline)

### Paycheck Breakdown & Statutory Deductions ($100 Gross Basis)
*Based on typical US median earner ($60,000/yr single filer, standard deduction):*
- **FICA Social Security (OASDI)**: 6.2% of gross earnings up to statutory wage base ($168,600).
- **FICA Medicare (HI)**: 1.45% of gross earnings (uncapped; +0.9% additional over $200k single).
- **Federal Income Tax (Effective Rate)**: ~9.5% – 12.0% for median single filer after standard deduction ($14,600).
- **State Income Tax (Median / Representative)**: 4.0% – 5.5% (State dependent; average state tax slice ~$4.50 per $100).
- **Take-Home (Net Pay)**: ~$76.00 – $78.00 per $100 earned before elective benefits (401k / health insurance).

### Retail Gasoline ($100 at the Pump Basis - EIA Data)
- **Crude Oil**: ~52% ($52.00)
- **Refining Costs & Margins**: ~19% ($19.00)
- **Distribution & Marketing**: ~14% ($14.00)
- **Federal & State Taxes**: ~15% ($15.00) (Federal excise: 18.4¢/gal + state average ~32.5¢/gal)

### Health Insurance Medical Loss Ratio (ACA 80/20 Rule - CMS)
- **Direct Medical Care & Clinical Services**: 80% to 85% ($80 to $85 per $100 of premiums)
- **Administrative Costs, Marketing, Profits**: 15% to 20% ($15 to $20 per $100 of premiums)
- Insurers failing the MLR threshold must rebate the difference directly to policyholders.

---

## 3. Production Fact-Check Log

| Date | Content Title | Key Statistics Used | Primary Source & URL | Verified By |
|---|---|---|---|---|
| 2026-11-10 | Short #1: Paycheck $100 | FICA 7.65% (6.2% SS + 1.45% Med), Fed eff ~10.5%, State avg ~4.5% | IRS Pub 15, SSA.gov, BLS | Agent QA |
