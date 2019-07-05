import React from 'react'
import PropTypes from 'prop-types'
import logoDark from './logo-greyscale.png'

function Footer(props) {
  const links = props.children && <>
    <h2 className="govuk-visually-hidden">Support links</h2>
    <ul className="hmlr-footer__links">
      {React.Children.map(props.children, (item, index) => (
        <li className="hmlr-footer__item" key={item.reactListKey}>
          {React.cloneElement(item, {className: 'hmlr-footer__link'})}
        </li>
      ))}
    </ul>
  </>

  let logo
  if (props.variant === 'dark') {
    logo = <img className="hmlr-footer__logo" width="172px" height="55px" src={logoDark} alt="HM Land Registry" />
  }

  return <footer className={`hmlr-footer hmlr-footer--${props.variant} ${props.classes}`}>
    <div className="hmlr-footer__inner">
      {logo}
      {links}
    </div>
  </footer>
}

Footer.defaultProps = {
  variant: 'white',
}

Footer.propTypes = {
  children: PropTypes.node,
  variant: PropTypes.string,
  classes: PropTypes.string,
}

export default Footer
