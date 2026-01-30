import {Composition} from 'remotion';
import {SwanLogo} from './SwanLogo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="SwanLogo"
        component={SwanLogo}
        durationInFrames={360}
        fps={60}
        width={800}
        height={640}
        defaultProps={{
          backgroundColor: '#0a1828',
        }}
      />
    </>
  );
};
