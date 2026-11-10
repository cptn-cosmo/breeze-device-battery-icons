# Maintainer: cptn-cosmo
pkgname=breeze-device-battery-icons
pkgver=1.0.0
pkgrel=1
pkgdesc="Breeze battery-level icons for wireless mice and keyboards"
arch=('any')
url="https://github.com/cptn-cosmo/breeze-device-battery-icons"
license=('LGPL-3.0-or-later')
depends=('breeze-icons')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('1c0fdff478fef54fb9508aceac6155e7aeb6f14e33190e021d407d7a67c85a13')

package() {
  cd "$pkgname-$pkgver"
  install -dm755 "$pkgdir/usr/share/icons"
  cp -r --no-preserve=ownership icons/breeze icons/breeze-dark "$pkgdir/usr/share/icons/"
  find "$pkgdir/usr/share/icons" -type d -exec chmod 755 {} +
  find "$pkgdir/usr/share/icons" -type f -exec chmod 644 {} +
  install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
}
