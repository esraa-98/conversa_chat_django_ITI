import { Box, CssBaseline } from "@mui/material";
import PrimaryAppBar from "../template/PrimaryAppBar";
import PrimaryDraw from "../template/PrimaryDraw";
import SecondaryDraw from "../template/SecondaryDraw";
import Main from "../template/Main";
import PopularChannels from "../components/PrimaryDraw/PopularChannels";
import ExploreCategories from "../components/SecondaryDraw/ExploreCategories";
import ExploreServers from "../components/Main/ExploreServers";
const Home = () => {
  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <PrimaryAppBar />
      <PrimaryDraw>
        <PopularChannels open={false} />
      </PrimaryDraw>
      <SecondaryDraw>
        <ExploreCategories />
      </SecondaryDraw>
      <Main>
        <ExploreServers/>
      </Main>
    </Box>
  );
};
export default Home;
