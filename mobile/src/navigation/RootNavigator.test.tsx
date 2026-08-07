import { ROOT_INITIAL_ROUTE_NAME } from './RootNavigator';

describe('RootNavigator', () => {
  it('uses Home as the initial route', () => {
    expect(ROOT_INITIAL_ROUTE_NAME).toBe('Home');
  });
});
