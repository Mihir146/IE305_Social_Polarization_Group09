# Open and run the product-launch model

**Model file:** `handoff_output/product_launch/CampusProductLaunch.alp`.

1. Download/copy the latest repository files to your Windows computer. Extract a ZIP before opening its contents.
2. In AnyLogic **8.9 PLE**, select **File → Open** and choose that `.alp` file. Accept an older-version conversion if offered.
3. In the Projects panel, expand the model, right-click **Simulation**, then **Run**. Press the play button if the simulation window is paused.
4. For the first check, keep **policyIndex=6**, **rep=1000**. Let the campaign reach **period 60**.
5. The matching standalone Java realization ends with **300 aware, 148 paid buyers, 12 free samples and ₹19,200 profit**. The approved grid run has now been observed and its actual export matches Java except cohort/runtime.
6. The console prints the absolute output location. Each successful run saves a summary CSV and a trajectory CSV in `product_output` beneath the engine's working directory.

If opening, compilation or execution fails, preserve the exact error text. The detailed guide is [ANYLOGIC_BUILD.md](handoff_output/product_launch/ANYLOGIC_BUILD.md). Its manual construction section is a fallback; start with the supplied model file.

The repository's `.html` files display charts or slides in a browser. They are support material. AnyLogic runs the `.alp`; the final submission also includes PowerPoint slides.

## Optional live-network version

Open `handoff_output/product_launch/CampusProductLaunch_LiveNetwork.alp` for the separately prepared network animation. It keeps the same defaults and expected financial result. Follow `LIVE_NETWORK.md`; its first actual engine run is tracked separately. To roll back, open the approved `CampusProductLaunch.alp`.
