/***** Tailwind config approximating Asana look *****/
module.exports = {
  content: [
    './index.html',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        asanaPrimary: '#3a258e',
        asanaSidebar: '#151b26',
        asanaBackground: '#f7f8fa',
      },
    },
  },
  plugins: [],
};
