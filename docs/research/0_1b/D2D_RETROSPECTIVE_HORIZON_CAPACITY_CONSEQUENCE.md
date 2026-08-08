# MIZAN-GATE 0.1B — D2D Retrospective-Horizon Capacity Consequence

## Status and scope

This is an additive, no-results engineering-capacity record created after the
formal F1.3A observation-horizon freeze.

It does not reopen or modify any F1.3A scientific decision.

It contains no predictive modeling and no predictive utility result.

## Trigger for this update

F1.3A formally froze the retrospective comparator as:

**R = Bitcoin block 575059**

The earlier F1.2C pre-provisioning baseline covered Bitcoin history through:

**block 487975**

Therefore the infrastructure plan must now account for a later controlled
historical ceiling before provisioning.

The scientific horizon determines the infrastructure requirement.

Infrastructure convenience must not modify the frozen scientific horizon.

## Additional historical range

Prior ceiling:

**487975**

Frozen retrospective ceiling:

**575059**

Additional blocks required:

**87084**

The frozen secondary relative horizon H+2016 does not supersede R as the
largest source-declared planning ceiling.

Using the prior source-declared Elliptic maximum target height of 487975:

**487975 + 2016 = 489991**

which remains below:

**575059**

Therefore R is the controlling pre-provisioning historical ceiling under the
currently frozen horizon design.

## Serialized-block engineering sensitivity

Pinned Bitcoin Core v31.1 source contains:

**MAX_BLOCK_SERIALIZED_SIZE = 4000000 bytes**

The source describes this constant as a serialized-block size limit used for
buffer-size purposes.

D2D uses the value only as an intentionally conservative engineering
sensitivity bound.

It is not a measurement of historical average block size.

It is not a prediction of actual disk growth.

Applying 4,000,000 bytes to every one of the 87,084 added blocks gives:

**348,336,000,000 bytes**

or:

**348.336 decimal GB**

This is deliberately extreme because it assumes every added block reaches the
selected serialized-size ceiling.

## Inherited F1.2C planning components

The sealed F1.2C planning model used:

- historical raw-chain allowance: 130 GB
- Bitcoin Core txindex reserve: 20 GB
- Core state/metadata reserve: 10 GB
- Blockbook RocksDB reserve: 180 GB
- PostgreSQL plus reconstruction artifacts: 50 GB
- temporary/log/build/workspace: 50 GB

Inherited component total:

**440 GB**

Inherited safety headroom:

**25%**

Inherited planning envelope:

**550 GB**

The prior 550-GB figure remains an accurate record of the assumptions under
which F1.2C was sealed.

D2D does not rewrite that historical record.

## Updated conservative sensitivity arithmetic

For the F1.3A retrospective ceiling, add the 348.336-GB maximum raw-block
increment sensitivity to the inherited components.

Updated raw-chain sensitivity allowance:

**130 + 348.336 = 478.336 GB**

Updated component total:

**440 + 348.336 = 788.336 GB**

Twenty-five-percent safety headroom:

**197.084 GB**

Updated conservative planning envelope:

**985.420 GB**

Again, 985.420 GB is not measured usage.

It is a deliberately conservative planning sensitivity constructed before
runtime provisioning.

## Consequence for a nominal 1-TB disk

For decimal planning:

**1 TB = 1000 GB**

Residual capacity above the updated 985.420-GB envelope is:

**14.580 GB**

or approximately:

**1.458% of nominal disk capacity**

Therefore a nominal 1-TB disk technically exceeds the arithmetic envelope but
does not provide a reasonable additional operational margin for the working
research baseline.

This distinction matters.

D2D does not claim that 1 TB is physically incapable of storing the actual
historical reconstruction.

Instead:

**1 TB is no longer recommended as the conservative working research baseline
under the frozen R requirement.**

The conclusion is based on planning margin, not measured exhaustion.

## Updated working research provisioning

The provisional working baseline is updated to:

- 32 GB RAM
- 8 vCPU
- 2 TB fast SSD
- dedicated x86_64 / AMD64 Linux

The RAM and CPU values remain engineering choices rather than measured minimum
requirements.

The disk change is the direct engineering consequence of the frozen
retrospective horizon.

For a nominal decimal 2-TB disk:

**2000 - 985.420 = 1014.580 GB**

remains above the conservative sensitivity envelope.

This does not establish that 2 TB is the minimum disk requirement.

## High-headroom configuration

The existing high-headroom compute option remains:

- 64 GB RAM
- 16 vCPU
- 2 TB fast SSD

The distinction between the working baseline and high-headroom configuration
is therefore currently compute headroom rather than disk capacity.

A larger disk may later be selected operationally, but D2D does not freeze a
larger scientific requirement without evidence.

## Important limitations

This capacity update does not measure:

- actual historical blk*.dat bytes through block 575059;
- actual Bitcoin Core txindex growth;
- actual Core chainstate size;
- actual Blockbook RocksDB size for the bounded historical range;
- PostgreSQL reconstruction size;
- temporary synchronization peaks;
- filesystem overhead;
- operating-system usage;
- runtime duration.

Those require provisioned runtime measurement.

The 348.336-GB increment must not be described as expected raw-chain growth.

The 985.420-GB envelope must not be described as measured disk usage.

The 2-TB recommendation must not be described as the final minimum VM.

## Scientific firewall

D2D makes no change to:

- H0;
- H+1;
- H+6;
- H+144;
- H+2016;
- R = 575059;
- future C definitions;
- future A_h definitions;
- future G_h definitions;
- cohort rules;
- split rules;
- predictive metrics;
- uncertainty procedures.

No horizon was selected or modified using capacity results.

## Predictive firewall

No predictive 0.1B model is executed.

D2D contains no:

- PR-AUC;
- ROC-AUC;
- predictive F1;
- alert-budget metric;
- graph-utility estimate;
- Delta_G estimate;
- retrospective inflation estimate.

The 0.1B breakthrough claim remains unestablished.

## Commercial firewall

The provisioning recommendation is a research-engineering decision.

It is not evidence of commercial product performance, market value, regulatory
acceptance, or customer willingness to pay.

Commercial claims remain downstream of scientific and empirical evidence.

## Gate conclusion

The frozen F1.3A retrospective comparator increases the controlled historical
planning ceiling from block 487975 to block 575059.

A deliberately conservative serialized-block sensitivity adds 348.336 GB to
the inherited component model and yields an updated 985.420-GB planning
envelope.

A nominal 1-TB disk technically clears that arithmetic envelope by only
14.580 GB and is therefore no longer recommended as the conservative working
research baseline.

The updated provisional working baseline is:

**32 GB RAM / 8 vCPU / 2 TB fast SSD**

Measured usage, final minimum infrastructure, and runtime performance remain
unresolved.

No predictive conclusion follows.
