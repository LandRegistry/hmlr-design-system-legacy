import React from 'react'
import logoDark from './logo-greyscale.svg'

function Footer(props) {
  const links = props.children && <>
    <h2 className='govuk-visually-hidden'>Support links</h2>
    <ul className='hmlr-footer__links'>
      {React.Children.map(props.children, (item, index) => (
        <li className='hmlr-footer__item' key={index}>
          {React.cloneElement(item, { className: 'hmlr-footer__link' })}
        </li>
      ))}
    </ul>
  </>

  var logo
  if (props.variant === 'dark') {
    logo = <img class="hmlr-footer__logo" src={logoDark} alt="HM Land Registry" />
  }

  return <footer className={`hmlr-footer hmlr-footer--${props.variant} ${props.classes}`}>
    <div className='hmlr-footer__inner'>
      {logo}
      {links}
    </div>
  </footer>
}

Footer.defaultProps = {
  variant: 'white'
}

export default Footer
