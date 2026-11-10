# Maintainer: cptn-cosmo
pkgname=breeze-device-battery-icons
pkgver=1.1.0
pkgrel=1
pkgdesc="Breeze battery-level icons for wireless mice, keyboards and headsets"
arch=('any')
url="https://github.com/cptn-cosmo/breeze-device-battery-icons"
license=('LGPL-3.0-or-later')
depends=('breeze-icons')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('c70bed85841d3bc1cbf1a64f3a71cdb9a8fcd13acb5451fe46a6b16cb4af46ae')

package() {
  cd "$pkgname-$pkgver"
  install -dm755 "$pkgdir/usr/share/icons"
  cp -r --no-preserve=ownership icons/breeze icons/breeze-dark "$pkgdir/usr/share/icons/"
  find "$pkgdir/usr/share/icons" -type d -exec chmod 755 {} +
  find "$pkgdir/usr/share/icons" -type f -exec chmod 644 {} +
  install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
}
